# -*- coding: utf-8 -*-
import sys, os #, getpass
from fabric import Connection, task
# from invoke import Responder
from fabric.config import Config
from invocations.console import confirm

PROJECT_NAME = ""
PROJECT_PATH = "~/{}".format(PROJECT_NAME)
REPO_URL = ""

def get_connection(ctx):
    try:
        return Connection(ctx.host, ctx.user, connect_kwargs=ctx.connect_kwargs)
    except Exception as e:
        print(e)
        return None

@task
def set_credentials(ctx, usr, host):
    """
        Set the username, host to connect and th ssh key location.
    """
    ctx.user = usr
    ctx.host = host
    # default ssh key should be automatically load, if not, you
    # either specify one in the followed code or by the -i parameter
    # on fab call on the shell
    
    # ctx.connect_kwargs.key_filename = "{}/.ssh/id_rsa.pub".format(os.path.expanduser("~"))

def connection_handler(ctx, usr, host):
    # check if ctx is Connection object or Context object
    # if Connection object then return the current connection
    # else set credentials and get connection
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        set_credentials(ctx, usr, host)
        conn = get_connection(ctx)
    return conn

@task
def pull(ctx, usr, host, compose="", branch="master"):
    """
        Pull from the current branch.
    """
    conn = connection_handler(ctx, usr, host)

    # cache git credentials
    # git_username = input("Username for 'https://gitlab.com': ")
    # git_password = getpass.getpass("Password for 'https://%s@gitlab.com': " % git_username)
    # git_watchers = [
    #     Responder(pattern = r"Username for .*", response="{}{}".format(git_username, "\n")), 
    #     Responder(pattern = r"Password for .*", response="{}{}".format(git_password, "\n"))
    # ]
    
    with conn.cd(PROJECT_PATH):
        conn.run("git pull origin {}".format(branch), pty=True, watchers=git_watchers)


@task
def checkout(ctx, branch=None):
    """
        Checkout to a different branch (should not be use by itself, deploy with a different source branch).
    """
    if branch is None:
        sys.exit("branch name is not specified")
    print("branch-name: {}".format(branch))
    conn = connection_handler(ctx, usr, host)
    with conn.cd(PROJECT_PATH):
        conn.run("git checkout {branch}".format(branch=branch))


@task
def clone(ctx, usr, host, compose="", branch=""):
    """
        Clone the proyect repository (should only be done once).
    """
    conn = connection_handler(ctx, usr, host)

    ls_result = conn.run("ls").stdout
    ls_result = ls_result.split("\n")
    if exists(PROJECT_NAME, ls_result):
        print("project already exists")
        return
    conn.run("git clone {} {}".format(REPO_URL, PROJECT_NAME), pty=True)

@task
def run_migrations(ctx, usr, host, compose="", branch=""):
    conn = connection_handler(ctx, usr, host)

    with conn.cd(PROJECT_PATH):
        conn.run("./execute_server backend manage migrate")


@task
def collect_statics(ctx, usr, host, compose="", branch=""):
    """[
        Collect statics for backend.
    """
    conn = connection_handler(ctx, usr, host)

    with conn.cd(PROJECT_PATH):
        conn.run("./execute_server backend manage collectstatic")

@task
def start(ctx, usr, host, compose="docker-compose-prod.yml", branch="master"):
    """
        Start docker containers.
    """
    conn = connection_handler(ctx, usr, host)
    
    with conn.cd(PROJECT_PATH):
        conn.run("docker-compose -f {} up -d".format(compose))


@task
def build_backend(ctx, usr, host, compose="", branch=""):
    conn = connection_handler(ctx, usr, host)
    
    with conn.cd(PROJECT_PATH):
        conn.run("./build_backend")


@task
def build_frontend(ctx, usr, host, compose="", branch=""):
    conn = connection_handler(ctx, usr, host)
    
    with conn.cd(PROJECT_PATH):
        conn.run("./build_frontend")

@task
def restart(ctx, usr, host, compose="docker-compose-prod.yml", branch="master"):
    """
        Restart docker containers.
    """
    conn = connection_handler(ctx, usr, host)

    print("restarting docker container...")
    with conn.cd(PROJECT_PATH):
        conn.run("docker-compose -f {} down --remove-orphans".format(compose))
        conn.run("docker-compose -f {} up -d".format(compose))


@task
def deploy(ctx, usr, host, compose="docker-compose-prod.yml", branch="master"):
    """
        Deploy proyect on the server with user interaction.
    """
    conn = connection_handler(ctx, usr, host)

    if not conn:
        sys.exit("\u274c Failed to connect to server")
    things_todo = []
    if confirm("Do you want to pull from git?", assume_yes=True):
        things_todo.append(pull)
    if confirm("Do you want to build backend?", assume_yes=False):
        things_todo.append(build_backend)
    if confirm("Do you want to build frontend", assume_yes=True):
        things_todo.append(build_frontend)
    if confirm("Do you want to run migrations?", assume_yes=False):
        things_todo.append(run_migrations)
    if confirm("Do you want to collect static files?", assume_yes=False):
        things_todo.append(collect_statics)
    if confirm("Do you want to restart the server?", assume_yes=True):
        things_todo.append(restart)

    for todo in things_todo:
        todo(conn, usr, host, compose, branch)
        print("{} {}".format(todo.__name__, "\u2705"))
    else:
        print("All jobs done \U0001f643")

@task
def shell(ctx, usr, host):
    import subprocess
    subprocess.call([
        'ssh', '-t', '-p', "22", usr + '@' + host,
        "cd %s && ./execute_server backend manage shell" % PROJECT_PATH
    ])

@task
def execute(ctx, usr, host, command, compose="docker-compose-prod.yml"):
    """
        Execute commands in the containers.
    """
    conn = connection_handler(ctx, usr, host)
    if not conn:
        sys.exit("\u274c Failed to connect to server")
    with conn.cd(PROJECT_PATH):
        conn.run("./execute_server {}".format(command))

@task
def get(ctx, usr, host, ifile, ofile=os.getcwd()):
    """
        Retrieve (download) a file from the server,
        from the given ifile parameters.
        By default the file is saved on the current directory.

        ifile: name/path of the file on the server.
        ofile: name/path of the local file after download. 
    """
    conn = connection_handler(ctx, usr, host)
    if not conn:
        sys.exit("\u274c Failed to connect to server")
    if confirm("File {} is going to be download and save under {}, do you want to proceed?".format(ifile, ofile)):
        print("Downloading file... \U0001f4c1")
        with conn.cd(PROJECT_PATH):
            conn.get(ifile, ofile)
    else:
        print("Aborted, everything stays the same. \U0001f610")

@task
def put(ctx, usr, host, ifile, ofile=PROJECT_PATH):
    """
        Upload a file to the server,
        from the given ifile parameters.
        By default the file is saved on the current directory.

        ifile: name/path of the local file to upload. 
        ofile: name/path of the file on the server after upload.
    """
    conn = connection_handler(ctx, usr, host)
    if not conn:
        sys.exit("\u274c Failed to connect to server")
    if confirm("File {} is going to be upload and save under {}, do you want to proceed?".format(ifile, ofile)):
        print("Uploading file... \U0001f4c1")
        with conn.cd(PROJECT_PATH):
            conn.put(ifile, ofile)
    else:
        print("Aborted, everything stays the same. \U0001f610")

# About me

Base project with basic DRF + React app, using containers with Docker and Docker Compose.

# Docker and Docker Compose installation

Install Docker:

- `https://docs.docker.com/install/`

After install Docker, proceed to install Docker Compose:

- `https://docs.docker.com/compose/install/`

#  Project configuration

Create a file inside `backend.hci` called `local_settings.py` and paste the code from `local_settings.example.py`
(if you don't have a sentry url/id, comment this code in your `local_settings.py` after paste)

Create a file in the root of the project (same level as README.md) called `.env`, paste the code from `.env.example` and fill it with your credentials

# Setup guide

### Development

Generate SSL certificates to enable HTTPS:
- `cd ssl`
- `./self_signed`

## Containers

Build the containers:

- `./build_backend`
- `./build_frontend --target=dev` for local development 
- `./build_frontend` for production or staging

Start all containers:

- `docker-compose -f docker-compose-dev.yml up`

- Or to run them in background:

  - `docker-compose -f docker-compose-dev.yml up -d`

Run migrations:

- `./execute backend manage migrate`

Go to your favorite browser (or not), and enter `localhost` on the url bar.

# Basic commands

## Frontend

Install frontend dependencies:

- `./execute frontend install`

Or a particular dependency:

- `./execute frontend install <dependency_name>`

## Backend

Stop all containers:

- `docker-compose -f docker-compose-dev.yml down`

Restart all containers:

- `docker-compose -f docker-compose-dev.yml restart`

Apply migrations to the DB:

- `./execute backend manage migrate`

Create django migrations:

- `./execute backend manage makemigrations`

Create a super-user:

- `./execute backend manage createsuperuser`

Collect static files:

- `./execute backend manage collectstatic`

Install backend dependencies:

- `./execute backend pipenv install <dependency_name>` # Not fully functional yet
-  Outside the container (in the host backend root folder):
    - `pipenv shell`
    - `pipenv install <dependency_name>`
- Then you have to build the backend again with `./build_backend`


# Project deployment

To deploy you need to have fabric (2.x) installed in your system (you can install it with pip install fabric, this should install both versions, 1.x and 2.x) and invocations, or the virtualenv activated (`pipenv shell` inside the root project folder).
On the project root folder:
- `fab -r ./fabfiles/ deploy --branch=branch-name --host=server-ip --usr=server-username`

Where:
- `deploy` is the function to run
- `branch` is the branch you want to deploy (for production this should always be master, and is default to that, so this parameter can be ommited)
- `host` is the ip or domeain name of the host you want to deploy to.
- `usr` is the server user name

To use a different ssh key or one stored in a folder different from the default one:
- `-i, --identity` add one of those parameters when calling fab, follow by the ssh path.
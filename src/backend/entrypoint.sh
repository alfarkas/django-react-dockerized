#!/bin/bash
echo $@
#exec pipenv --venv
if [ $1 = "start_celery" ]
then
    exec celery -A project $2 --loglevel=info --sentry "$(cat /run/secrets/sentry)"
fi
if [ $1 = "start" ]
then
    exec pwd
    exec pipenv shell
    exec pipenv install --system
fi
if [ $1 = "manage" ]
then
    shift
    #exec pipenv run python manage.py $@
    exec python manage.py $@
elif [ $1 = "install" ]
then
    shift
    #cd /usr/src
    exec pipenv install $@
else
    #exec pipenv run $@
    exec $@
fi
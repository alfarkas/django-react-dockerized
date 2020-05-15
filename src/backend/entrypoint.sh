#!/bin/bash
if [ $1 = "start" ]
then
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
    exec pipenv install $@
elif [ $1 = "rungunicorn" ]
then
    shift
    cpus="$(nproc --all)"
    workers="$((($cpus * 2) + 1))"
    if [ $workers -gt 12 ]
    then
        workers="12"
    fi
    exec gunicorn hci.wsgi:application --bind 0.0.0.0:8000 --workers $workers
else
    #exec pipenv run $@
    exec $@
fi
#!/bin/bash
echo $@
#exec pipenv --venv
if [ $1 = "start" ]
then
    echo "start"
    exec pwd
    exec pipenv shell
    exec pipenv install --system
fi
if [ $1 = "manage" ]
then
    echo "entra"
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
    echo "no entra"
fi
echo "naskdjs"
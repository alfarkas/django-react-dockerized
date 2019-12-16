#!/bin/sh
if [ $1 == "install" ]
then
    shift
    #cd /usr/src
    exec npm install $@
else
    exec $@
fi
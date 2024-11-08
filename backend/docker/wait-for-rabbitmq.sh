#!/bin/bash

set -e

HOST=$1
PORT=$2

while ! nc -z $HOST $PORT
do
    echo "$(date) - waiting for rabbitmq to start"
    sleep 3
done

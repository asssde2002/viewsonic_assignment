#!/bin/bash

cd backend

# double check python dependencies
pip install -r requirements.txt

# wait for RabbitMQ server and Database to start
bash ./docker/wait-for-postgres.sh db 5432
bash ./docker/wait-for-rabbitmq.sh rabbitmq 5672

celery --app celery_app flower

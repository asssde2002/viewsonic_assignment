#!/bin/bash

cd backend

# double check python dependencies
pip install -r requirements.txt

# wait for RabbitMQ server and Database to start
bash ./docker/wait-for-postgres.sh db 5432
bash ./docker/wait-for-rabbitmq.sh rabbitmq 5672

watchmedo auto-restart -d ./ -R -p '*.py' -- celery --app celery_app worker --loglevel info --prefetch-multiplier 0 --concurrency 1 -Q celery,viewsonic_pq

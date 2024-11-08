#!/bin/bash

cd backend

# double check python dependencies
pip install -r requirements.txt
# wait for RabbitMQ server and Database to start
bash ./docker/wait-for-postgres.sh db 5432
bash ./docker/wait-for-rabbitmq.sh rabbitmq 5672

# gunicorn -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app --reload
alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

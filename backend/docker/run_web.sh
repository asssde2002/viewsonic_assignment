#!/bin/bash

pip install -r requirements.txt
bash ./docker/wait-for-postgres.sh db 5432
gunicorn -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app --reload

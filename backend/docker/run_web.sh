#!/bin/bash

bash ./docker/wait-for-postgres.sh db 5432
gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app

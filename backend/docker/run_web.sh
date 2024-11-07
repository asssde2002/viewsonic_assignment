#!/bin/bash

bash ./docker/wait-for-postgres.sh db 6432
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

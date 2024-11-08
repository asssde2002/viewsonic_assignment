FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y postgresql-client gcc netcat-traditional

WORKDIR /app

COPY ./backend /app/backend
COPY ./frontend /app/frontend

RUN pip install -r /app/backend/requirements.txt
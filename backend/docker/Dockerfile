FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt
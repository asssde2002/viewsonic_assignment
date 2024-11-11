# viewsonic_assignment
# How to start the services
1. `docker-compose build --no-cahce`
2. `docker-compose up`
3. `open http://localhost:8000`

# Migration
1. `alembic revision --autogenerate -m "xxxxxxx"`
2. `alembic upgrade head`

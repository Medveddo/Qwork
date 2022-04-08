# Text analysis system (Bachelor's qualification work in NSTU)

`uvicorn app.main:app`

`dramatiq app.dramatiq:DRAMATIQ_REDIS_BROKER app.tasks`

`python -m app.scheduler`

## Description

Expected and stack that I want to use in this project:

- Backend: FastAPI
- Database: PostgreSQL and MongoDB
- Metrics and Monitoring: Prometheus and Grafana
- Background and delayed tasks: Dramatiq
- Scheduling: APScheduler
- Cache system and message broker: Redis
- Frontend: Mithril or Svetle
- Natural language processing: Natasha
- Logging: Fluentd
- Web-server: Caddy/Nginx

Also want deploy to Kubernetes

## Formating

`black . --check && flake8`

## Alembic

`alembic revision --autogenerate -m 'initial'`

`alembic upgrade head`

`alembic downgrade base`

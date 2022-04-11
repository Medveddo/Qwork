# Text analysis system (Bachelor's qualification work in NSTU)

## How to run

Create .env file with variables:

```dotenv
DATABASE_URL=postgresql://postgres:postgres@db:5432/qwork
DRAMATIQ_BROKER_URL=redis://redis:6379/0
POSTGRES_DB=qwork
POSTGRES_PASSWORD=postgres
POSTGRES_USER=postgres
VITE_API_URL=http://localhost:8000/api/
VITE_ENVIRONMENT=local
```

Docker compose up:

```shell
docker-compose --file docker-compose.local.yaml up --build
```

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

## TODO Checklist

✅| Prometheus + Grafana

✅| CloudBeaver

✅| FluentBit + Zinc

✅| Patient table in Postgres

✅| SQLAlchemy Relation between ProcessTextRun and Patient

✅| Rename ProcessTextRun to Run

⬜️| Split requirements

⬜️| Pytest

⬜️| [Implement HashIDs](https://github.com/davidaurelio/hashids-python)

⬜️| Move API from qwork.sizikov.space/api/ to api.qwork.sizikov.space

⬜️| Periodic processing jobs

⬜️| Paper - Title page

⬜️| Paper - Introduction (Relevance, goals, ...)

⬜️| Actions with patients from Frontend (run individual record)

⬜️| Run backend application in MiniKube

⬜️| [Fancy frontend (try tailwind ui components ?)](https://tailwindui.com/#components)

⬜️| Another important feature ...

✅| Drink some water

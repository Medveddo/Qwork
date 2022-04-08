# Text analysis system (Bachelor's qualification work in NSTU)

## Local .env file

```dotenv
DATABASE_URL=postgresql://postgres:postgres@db:5432/qwork
DRAMATIQ_BROKER_URL=redis://redis:6379/0
POSTGRES_DB=qwork
POSTGRES_PASSWORD=postgres
POSTGRES_USER=postgres
VITE_API_URL=http://localhost:8000/api/
VITE_ENVIRONMENT=local
```

`docker-compose --file docker-compose.local.yaml up --build

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

## Local start

1. Copy data from Caddyfile_local to Caddyfile
2. Set `var backend_url = "localhost:8000/api";` in frontend/index.js file
2.1 replace all https with http
3. Expose only :80 port of frontend container to any of your machine ports (for me 80:80 does not works on Debian)

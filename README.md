# Text analysis system (Bachelor's qualification work in NSTU)

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
3. Expose only :80 port of frontend container to any of your machine ports (for me 80:80 does not works on Debian)

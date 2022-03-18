#!/usr/bin/env bash

./scripts/wait-for-it.sh db:5432 -t 15
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000
#!/usr/bin/env bash

./scripts/wait-for-it.sh db:5432 -t 15
./scripts/wait-for-it.sh redis:6379 -t 15
./scripts/wait-for-it.sh backend:8000 -t 15

python -m app.commands.simulate_activity

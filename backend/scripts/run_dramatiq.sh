#!/usr/bin/env bash

./scripts/wait-for-it.sh db:5432 -t 15
./scripts/wait-for-it.sh redis:6379 -t 15

dramatiq app.dramatiq:DRAMATIQ_BROKER app.tasks --watch app --processes 1 --threads 1

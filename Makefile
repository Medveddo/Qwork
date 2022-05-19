docker:
	# docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres --name postgres -e POSTGRES_DB=qwork  postgres:alpine
	# docker run -d -p 6379:6379 --name reids redis:alpine
	bash -c "docker start redis postgres"

fast:
	bash -c "cd backend && venv/bin/uvicorn app.main:app --reload"

drama:
	bash -c "cd backend && venv/bin/dramatiq app.dramatiq:DRAMATIQ_BROKER app.tasks -t 1 -p 1 --watch app"

front:
	bash -c "cd frontend && npm run dev"

migrations:
	bash -c "cd backend && venv/bin/alembic revision --autogenerate"

migrate:
	bash -c "cd backend && venv/bin/alembic upgrade head"

scheduler:
	bash -c "cd backend && venv/bin/python -m app.scheduler"

simulate:
	bash -c "cd backend && venv/bin/python app/commands/simulate_activity.py"

nlp:
	bash -c "cd backend && venv/bin/python app/nlp.py"

docker:
	# docker run -d -e MONGO_INITDB_ROOT_USERNAME=mongo -e MONGO_INITDB_ROOT_PASSWORD=mongo -p 27017:27017 --name mongo mongo
	# docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mongo
	# docker run -d -e ME_CONFIG_MONGODB_ADMINUSERNAME=mongo -e ME_CONFIG_MONGODB_ADMINPASSWORD=mongo -e ME_CONFIG_MONGODB_URL=mongodb://mongo:mongo@172.17.0.4:27017/ -p 8081:8081 --name mongo-express mongo-express
	# docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres --name postgres -e POSTGRES_DB=qwork  postgres:alpine
	# docker run -d -p 6379:6379 --name reids redis:alpine
	bash -c "docker start redis postgres"

fast:
	bash -c "cd backend && venv/bin/uvicorn app.main:app --reload"

black:
	bash -c "cd backend && venv/bin/black ."

flake:
	bash -c "cd backend && venv/bin/flake8"

test:
	bash -c "cd backend && venv/bin/pytest"

testall:
	bash -c "cd backend && venv/bin/coverage run -m pytest --no-testmon && venv/bin/coverage report && venv/bin/coverage html"

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

lint:
	bash -c "cd backend && venv/bin/isort ."
	bash -c "cd backend && venv/bin/black ."
	bash -c "cd backend && venv/bin/flake8"

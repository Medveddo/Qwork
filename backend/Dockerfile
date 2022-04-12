FROM python:3.10-slim

WORKDIR /app

COPY ./requirements/base.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./scripts /app/scripts
RUN chmod +x /app/scripts/wait-for-it.sh && \
    chmod +x /app/scripts/run.sh && \
    chmod +x /app/scripts/run_dramatiq.sh && \
    chmod +x /app/scripts/run_scheduler.sh

COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini
COPY ./app /app/app
    
CMD ["scripts/run.sh"]

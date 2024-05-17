FROM python:3.10.8

WORKDIR /app

ARG POSTGRES_URL
ARG BANK_URL
ARG REDIS_URL

ENV PYTHONUNBUFFERED 1
ENV POSTGRES_URL=$POSTGRES_URL
ENV BANK_URL=$BANK_URL
ENV REDIS_URL=$REDIS_URL

RUN pip install --upgrade pip
RUN pip install --no-cache-dir poetry psycopg2-binary

COPY ./poetry.lock /app/poetry.lock
COPY ./pyproject.toml /app/pyproject.toml

RUN poetry export --without-hashes -f requirements.txt --output requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT celery -A main beat --loglevel=info & celery -A main worker --loglevel=info
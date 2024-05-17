FROM python:3.10.8

WORKDIR /app

ARG POSTGRES_URL
ARG SECRET_KEY
ARG DEBUG

ENV PYTHONUNBUFFERED 1
ENV POSTGRES_URL=$POSTGRES_URL
ENV SECRET_KEY=$SECRET_KEY
ENV DEBUG=$DEBUG

RUN pip install --upgrade pip
RUN pip install --no-cache-dir poetry psycopg2-binary

COPY ./poetry.lock /app/poetry.lock
COPY ./pyproject.toml /app/pyproject.toml

RUN poetry export --without-hashes -f requirements.txt --output requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/run.sh
CMD /app/run.sh
FROM python:3.11.3-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/jobs-api

COPY pyproject.toml poetry.lock ./

RUN pip install poetry==1.4.1 &&  \
    poetry config virtualenvs.create false &&  \
    poetry install --only main

#COPY ./jobs_api/ ./migrations/ ./alembic.ini ./

COPY . .
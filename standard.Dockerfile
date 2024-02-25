# syntax=docker/dockerfile:1

ARG PYTHON_REGISTRY=python
ARG PYTHON_VERSION=3.10.13
FROM ${PYTHON_REGISTRY}:${PYTHON_VERSION}-alpine as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

RUN python -m pip install wheel poetry==1.7.1

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev,test && rm -rf $POETRY_CACHE_DIR

COPY src ./src
RUN poetry install --without dev,test --no-root

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

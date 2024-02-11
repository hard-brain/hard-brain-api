# syntax=docker/dockerfile:1

ARG PYTHON_REGISTRY=python
ARG PYTHON_VERSION=3.10.13
FROM ${PYTHON_REGISTRY}:${PYTHON_VERSION}-alpine as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
RUN apk update && apk add \
    gcc \
    libc-dev \
    libffi-dev \
    libressl-dev \
    musl-dev \
    libffi-dev \
    gcompat \
    cargo
# RUN python -m pip install wheel poetry==1.7.1
# RUN apk del \
#     gcc \
#     libc-dev \
#     libffi-dev \
#     libressl-dev \
#     musl-dev \
#     libffi-dev \
#     gcompat \
#     cargo

COPY requirements.txt .
RUN pip install --upgrade setuptools wheel && pip install -r requirements.txt

COPY src ./src

EXPOSE 8000

CMD ["python", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

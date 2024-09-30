FROM python:3.11.9-alpine3.20
EXPOSE 8080

WORKDIR /usr/backend_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/usr/app/.

RUN apk update
RUN apk add --no-cache build-base
RUN apk add --no-cache bash
RUN apk add --no-cache curl

RUN pip install --upgrade pip
RUN pip install poetry

COPY . .

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi
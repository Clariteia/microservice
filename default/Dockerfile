FROM python:slim-buster as build

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install --yes postgresql-client git curl netcat

# Install and setup poetry
RUN pip install -U pip \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"

WORKDIR /microservice

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . .
RUN poetry build

FROM python:slim-buster as deploy

COPY --from=build /microservice/dist/ ./dist

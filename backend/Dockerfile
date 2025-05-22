FROM python:3.13-slim

ENV POETRY_VERSION=1.8.2

RUN apt-get update && apt-get install -y curl postgresql-client && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app
COPY . .

RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]

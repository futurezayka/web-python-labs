ARG PYTHON_VERSION=3.12.0
FROM python:${PYTHON_VERSION}-slim as base

WORKDIR /app

ENV PYTHONPATH .

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --only main || echo "Poetry install failed"

COPY . .

RUN chmod +x ./app-start.sh
CMD ["./app-start.sh"]

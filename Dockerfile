FROM python:3.12.9-slim
WORKDIR /app

ENV PYTHONPATH .

# RUN apt-get update -y && apt-get install -y build-essential postgresql pkg-config default-libmysqlclient-dev awscli git

RUN pip install poetry
RUN pip install --upgrade pip setuptools wheel

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --only main || echo "Poetry install failed" \

COPY . .

EXPOSE 8000

CMD ["./app-start.sh"]
FROM python:3.12-slim

WORKDIR /app

# Устанавливаем зависимости системы (например, для psycopg2)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Копируем только файлы, нужные для Poetry
COPY pyproject.toml poetry.lock /app/

# Устанавливаем Poetry и зависимости проекта (без установки самого проекта)
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi --no-root

# Копируем весь код проекта после установки зависимостей
COPY . /app/

# Теперь устанавливаем сам проект
RUN poetry install --no-interaction --no-ansi --no-root


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

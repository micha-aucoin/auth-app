FROM python:3.10-slim-buster

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.4.2

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /auth-app/
COPY poetry.lock pyproject.toml /auth-app/

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /auth-app/

ENV API_V1_PREFIX="/api/v1" \
    DEBUG=True \
    PROJECT_NAME="Heroes App (local)" \
    VERSION="0.1.0" \
    DESCRIPTION="The API for Authentication app." \
    PG_DRIVER="postgresql+asyncpg" \
    PG_USERNAME="admin" \
    PG_PASSWORD="thepass123" \
    PG_HOST='users-pg' \
    PG_PORT="5432" \
    PG_DATABASE="users_db" \
    DB_EXCLUDE_TABLES="[]" \
    JWT_SECRET="eb9fdf01e4f1b556cde951d1ac4e5ad3dd519bc6f0ed67f8fb8a54e757144b1d"

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 80"]

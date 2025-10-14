# Open Heavens API

FastAPI-based devotional API using Domain-Driven Design (DDD) and CQRS-friendly structure.

Quick start

1. Copy .env.example to .env and set values
2. poetry install
3. Run DB migration: psql -d <db> -f sql/init_schema.sql
4. Start server: poetry run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

Docker (quick local dev)

1. docker compose up --build
2. App will be on http://localhost:8000, pgAdmin on http://localhost:8080 (user: admin@local / password: admin)

Alembic

- Alembic scaffold is included (edit `alembic.ini` sqlalchemy.url). Use `poetry run alembic revision -m "msg" --autogenerate` and `poetry run alembic upgrade head` to run migrations.

Security

All requests must include header X-API-Key with the value from the `API_KEY` env var.

Notes

- Uses psycopg 3
- Minimal tests included

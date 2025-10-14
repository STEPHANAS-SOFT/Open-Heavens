#!/usr/bin/env bash
# Small helper to run the app with uvicorn
export $(cat .env | xargs)
poetry run uvicorn app.main:app --reload --host ${UVICORN_HOST:-127.0.0.1} --port ${UVICORN_PORT:-8000}

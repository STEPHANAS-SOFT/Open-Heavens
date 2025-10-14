import os
import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_without_key():
    resp = client.get("/health")
    assert resp.status_code == 200


def test_protected_requires_key():
    # no api key header
    resp = client.get("/hymns/")
    # FastAPI returns 422 if required header missing
    assert resp.status_code in (401, 422)


def test_with_invalid_key():
    resp = client.get("/hymns/", headers={"X-API-Key": "wrong"})
    assert resp.status_code == 401


def test_with_bearer_header_format():
    # Ensure Bearer <token> format is handled (will be rejected if token wrong)
    resp = client.get("/hymns/", headers={"Authorization": "Bearer wrong"})
    assert resp.status_code in (401, 422)

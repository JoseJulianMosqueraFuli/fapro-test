import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_uf_valid_date():
    payload = {"date": "2022-05-15"}
    response = client.post("/uf", json=payload)
    assert response.status_code == 200
    assert "uf_value" in response.json()


def test_uf_invalid_date():
    payload = {"date": "2022-02-30"}  # Invalid date: February 30th
    response = client.post("/uf", json=payload)
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "Día inválido" in response.json()["detail"]


def test_uf_missing_date():
    payload = {}  # Missing "date" key
    response = client.post("/uf", json=payload)
    assert response.status_code == 422
    assert "detail" in response.json()
    assert "field required" in response.json()["detail"][0]["msg"]


def test_uf_empty_date():
    payload = {"date": ""}
    response = client.post("/uf", json=payload)
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "Fecha inválida" in response.json()["detail"]


def test_uf_invalid_format():
    payload = {"date": "2022/05/15"}  # Invalid format: using slashes instead of dashes
    response = client.post("/uf", json=payload)
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "Fecha inválida" in response.json()["detail"]


def test_uf_invalid_before_year():
    payload = {"date": "2000-05-15"}  # Invalid year: 2000 (before 2013)
    response = client.post("/uf", json=payload)
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "Año inválido" in response.json()["detail"]


def test_uf_invalid_after_year():
    payload = {"date": "2024-05-15"}  # Invalid year: 2000 (before 2013)
    response = client.post("/uf", json=payload)
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "Año inválido" in response.json()["detail"]

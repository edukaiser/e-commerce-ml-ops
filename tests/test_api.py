"""Módulo de testes automatizados para a API FastAPI."""

from fastapi.testclient import TestClient
from src.api.main import app


def test_health_check() -> None:
    """Testa se a rota principal está online."""
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {
            "status": "online",
            "message": "API de recomendação rodando!",
        }


def test_predict_endpoint() -> None:
    """Testa se o endpoint de predição retorna a estrutura esperada."""
    with TestClient(app) as client:
        payload = {"user_idx": 345, "item_idx": 645}
        response = client.post("/predict", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "user_idx" in data
        assert "item_idx" in data
        assert "predicted_score" in data
        assert isinstance(data["predicted_score"], float)

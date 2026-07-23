"""Módulo da API de Inferência utilizando FastAPI.

Este módulo expõe os endpoints para predição do modelo de recomendação PyTorch.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import torch.nn as nn


class RecommendationMLP(nn.Module):
    """Arquitetura Multi-Layer Perceptron para recomendação baseada em embeddings."""

    def __init__(self, num_users: int, num_items: int, embedding_dim: int = 32) -> None:
        """Inicializa as camadas de embedding e a estrutura interna da rede."""
        super().__init__()
        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.item_embedding = nn.Embedding(num_items, embedding_dim)
        self.fc_layers = nn.Sequential(
            nn.Linear(embedding_dim * 2, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        )

    def forward(self, user_idx: torch.Tensor, item_idx: torch.Tensor) -> torch.Tensor:
        """Executa a passagem para frente (forward pass) da rede."""
        user_vector = self.user_embedding(user_idx)
        item_vector = self.item_embedding(item_idx)
        x = torch.cat([user_vector, item_vector], dim=-1)
        return torch.sigmoid(self.fc_layers(x).squeeze(-1))


app = FastAPI(
    title="API de Recomendação - E-commerce MLOps",
    description="API para inferência do modelo de Deep Learning (PyTorch)",
    version="1.0.0",
)

model: nn.Module | None = None
NUM_USERS = 190804
NUM_ITEMS = 49841


@app.on_event("startup")
def load_model() -> None:
    """Carrega os pesos do modelo treinado na inicialização da aplicação."""
    global model
    model = RecommendationMLP(
        num_users=NUM_USERS, num_items=NUM_ITEMS, embedding_dim=32
    )
    try:
        model.load_state_dict(
            torch.load(
                "models/recommender_model.pt",
                map_location=torch.device("cpu"),
                weights_only=True,
            )
        )
        model.eval()
        print("Modelo carregado com sucesso na inicialização da API!")
    except Exception as e:
        print(f"Erro ao carregar os pesos do modelo: {e}")


class RecommendationRequest(BaseModel):
    """Esquema de dados para a requisição de predição."""

    user_idx: int
    item_idx: int


@app.get("/")
def health_check() -> dict[str, str]:
    """Verifica se a API está online."""
    return {"status": "online", "message": "API de recomendação rodando!"}


@app.post("/predict")
def predict(payload: RecommendationRequest) -> dict[str, int | float]:
    """Realiza a predição de pontuação para o par usuário-item."""
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo não carregado.")

    user_tensor = torch.tensor([payload.user_idx], dtype=torch.long)
    item_tensor = torch.tensor([payload.item_idx], dtype=torch.long)

    with torch.no_grad():
        prediction = model(user_tensor, item_tensor)
        score = float(prediction.item())

    return {
        "user_idx": payload.user_idx,
        "item_idx": payload.item_idx,
        "predicted_score": round(score, 4),
    }

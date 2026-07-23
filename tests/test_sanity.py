"""Módulo de testes de sanidade e estabilidade para o modelo."""

import torch
from src.models.model import RecommendationMLP


def test_model_sanity_and_bounds() -> None:
    """Garante que a saída do modelo está estritamente entre 0 e 1 (Sigmoid)."""
    model = RecommendationMLP(num_users=100, num_items=100)
    model.eval()

    users = torch.randint(0, 100, (50,))
    items = torch.randint(0, 100, (50,))

    with torch.no_grad():
        preds = model(users, items)

    # Verifica se não há valores NaN ou infinitos
    assert not torch.isnan(preds).any()
    assert not torch.isinf(preds).any()

    # Como é recomendação com BCELoss, a saída deve estar normalizada entre 0 e 1
    assert preds.min() >= 0.0
    assert preds.max() <= 1.0

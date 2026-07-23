"""Módulo contendo a arquitetura do modelo de recomendação baseado em PyTorch."""

import torch
import torch.nn as nn


class RecommendationMLP(nn.Module):
    """Arquitetura Multi-Layer Perceptron para recomendação baseada em embeddings.

    Esta rede utiliza camadas de embedding para representar usuários e itens,
    combinando-os através de uma MLP para prever o score de preferência.

    Args:
        num_users (int): Quantidade total de usuários únicos.
        num_items (int): Quantidade total de itens únicos.
        embedding_dim (int, optional): Dimensão do vetor de embedding. Padrão é 32.
    """

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
        """Executa a passagem para frente (forward pass) da rede.

        Args:
            user_idx (torch.Tensor): Tensor contendo os índices dos usuários.
            item_idx (torch.Tensor): Tensor contendo os índices dos itens.

        Returns:
            torch.Tensor: Scores de probabilidade previstos pela rede (0 a 1).
        """
        user_vector = self.user_embedding(user_idx)
        item_vector = self.item_embedding(item_idx)
        x = torch.cat([user_vector, item_vector], dim=-1)
        # Aplicando a sigmoid para normalizar a saída entre 0 e 1
        return torch.sigmoid(self.fc_layers(x).squeeze(-1))

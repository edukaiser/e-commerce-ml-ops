"""Módulo de Treinamento utilizando PyTorch.

Este módulo implemente a arquiterura de uma rede neural MLP para recomendação,
utilizando o padrão de projeto Factory para inicialização de componentes.
"""

from abc import ABC, abstractmethod
import pathlib
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
import mlflow


class RecommendationMLP(nn.Module):
    """Arquitetura Multi-Layer Perceptron para recomendação baseada em embeddings."""

    def __init__(self, num_users: int, num_items: int, embedding_dim: int = 32) -> None:
        """Inicializa as camadas de embedding e a estrutura interna da rede."""
        super().__init__()
        # Camadas de embedding que transformarão os índices densos em vetores numéricos
        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.item_embedding = nn.Embedding(num_items, embedding_dim)

        # Camadas lineares da MLP (Combina os embeddings e reduz até a previsão final)
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

        # Concatena os vetores do usuário e do item lado a lado
        x = torch.cat([user_vector, item_vector], dim=-1)
        return self.fc_layers(x).squeeze(-1)


class ModelFactory(ABC):
    """Fábrica abstrata para garantir o padrão Factory exigido no edital."""

    @abstractmethod
    def create_model(self, num_users: int, num_items: int) -> nn.Module:
        """Cria e retorna a instância do modelo PyTorch."""
        pass


class SimpleModelFactory(ModelFactory):
    """Fábrica concreta para instanciar a nossa RecommendationMLP."""

    @abstractmethod
    def create_model(self, num_users: int, num_items: int) -> nn.Module:
        """Instancia a MLP com dimensões fixas ou parametrizadas."""
        return RecommendationMLP(
            num_users=num_users, num_items=num_items, embedding_dim=32
        )


def main() -> None:
    """Função principal para executar a preparação do treinamento."""
    print("====== INICIANDO ESTÁGIO: TRAIN ======")

    # 1. Carrega o output do estágio de feature engineering
    input_path = "data/processed/features_ready.csv"
    print(f"Lendo dados processados de {input_path}")
    df = pd.read_csv(input_path)

    # 2. Descobre o número de usuários e itens para dimensão dos Embeddings
    num_users = int(df["user_idx"].max() + 1)
    num_items = int(df["item_idx"].max() + 1)
    print(f"Detectados {num_users} usuários e {num_items} itens únicos.")

    # 3. Usa o Design Pattern Factory para instanciar a rede reural
    factory = SimpleModelFactory()
    model = factory.create_model(num_users, num_items)
    print(f"Modelo instanciado via Factory com sucesso:\n{model}")

    # 4. Garante a criação da pasta models e salva um esqueleto do modelo
    pathlib.Path("models").mkdir(parents=True, exist_ok=True)

    # Converte as colunas do pandas para tensores do PyTorch
    X_user = torch.tensor(df["user_idx"].values, dtype=torch.long)
    X_item = torch.tensor(df["item_idx"].values, dtype=torch.long)
    y = torch.tensor(df["target"].values, dtype=torch.float32)

    dataset = TensorDataset(X_user, X_item, y)
    dataloader = DataLoader(dataset, batch_size=1024, shuffle=True)

    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # 5. Inicializa o monitoramento do experimento no MLflow
    mlflow.set_experiment("Recomendador_RetailRocket")

    with mlflow.start_run(run_name="treino_base_pytorch"):
        epochs = 3
        mlflow.log_param("embedding_dim", 32)
        mlflow.log_param("epochs", epochs)
        mlflow.log_param("batch_size", 1024)
        mlflow.log_param("lr", 0.001)

        print("Iniciando loop de treinamento...")
        model.train()
        for epoch in range(epochs):
            epoch_loss = 0.0
            for batch_user, batch_item, batch_target in dataloader:
                optimizer.zero_grad()
                predictions = model(batch_user, batch_item)
                loss = criterion(predictions, batch_target)
                loss.backward()
                optimizer.step()

                epoch_loss += loss.item() * batch_user.size(0)

            total_epoch_loss = epoch_loss / len(dataset)
            print(f"Época [{epoch + 1}/{epochs}] - Perda (MSE): {total_epoch_loss:.4f}")
            mlflow.log_metric("mse_loss", total_epoch_loss, step=epoch)

        # Salva os pesos finais do modelo treinado
        model_path = "models/recommender_model.pt"
        torch.save(model.state_dict(), model_path)

        # Registra o arquivo gerado dentro do MLflow
        mlflow.log_artifact(model_path)
        print("Modelo treinado e artefatos salvos com sucesso!")

    print("====== ESTÁGIO TRAIN CONCLUÍDO ======\n")


if __name__ == "__main__":
    main()

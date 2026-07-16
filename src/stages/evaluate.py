import json
import torch
import pandas as pd
from sklearn.metrics import mean_squared_error
from src.models.model import RecommendationMLP


def evaluate_model(
    model_path: str,
    test_data_path: str,
    output_metrics_path: str,
) -> None:
    """Avalia o modelo e salva métricas em um arquivo JSON."""
    # Carrega os dados primeiro para saber o tamanho da arquitetura
    df_test = pd.read_csv(test_data_path)
    num_users = int(df_test["user_idx"].max() + 1)
    num_items = int(df_test["item_idx"].max() + 1)

    # Instancia a classe do modelo com as dimensões corretas
    model = RecommendationMLP(num_users=num_users, num_items=num_items)

    # Carrega apenas os pesos (state_dict) no modelo instanciado
    model.load_state_dict(torch.load(model_path))

    model.eval()

    # Lógica de predição para avaliação
    user_tensor = torch.tensor(df_test["user_idx"].values, dtype=torch.long)
    item_tensor = torch.tensor(df_test["item_idx"].values, dtype=torch.long)

    with torch.no_grad():
        predictions = model(user_tensor, item_tensor)

    # Cálculo de Métrica
    mse = mean_squared_error(df_test["target"], predictions.numpy())

    # Salva métricas para o DVC monitorar
    metrics = {"rmse": float(mse**0.5)}
    with open(output_metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)


if __name__ == "__main__":
    evaluate_model(
        model_path="models/recommender_model.pt",
        test_data_path="data/processed/features_ready.csv",
        output_metrics_path="reports/metrics.json",
    )

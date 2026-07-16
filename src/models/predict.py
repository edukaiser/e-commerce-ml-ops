import torch
from src.schema import RecommenderInput


class ModelWrapper:
    """Wrapper para carregar e realizar predições com o modelo PyTorch."""

    def __init__(self, model_path: str = "models/recommender_model.pt") -> None:
        """Inicializa o modelo."""
        self.model = torch.load(model_path)
        self.model.eval()

    def predict(self, input_data: RecommenderInput) -> torch.Tensor:
        """Realiza a predição baseada no input validado.

        Args:
            input_data: Dados de entrada validados pelo schema.

        Returns:
            O resultado da inferência do modelo.
        """
        # O modelo espera os IDs como tensores separados (comuns em
        # arquiteturas de recsys)
        user_tensor = torch.tensor([input_data.user_idx], dtype=torch.long)
        item_tensor = torch.tensor([input_data.item_idx], dtype=torch.long)

        # Lógica de inferência garantindo tipo tensor
        with torch.no_grad():
            output = self.model(user_tensor, item_tensor)

        return output

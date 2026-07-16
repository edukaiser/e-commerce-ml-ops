import torch
from src.schema import RecommenderInput


class Predictor:
    """Motor de inferência que não depende de arquivos externos."""

    def __init__(self, model: torch.nn.Module, device: str = "cpu") -> None:
        """Inicializa o preditor com um modelo pré-carregado.

        Args:
            model: Instância do modelo PyTorch (já carregado com pesos).
            device: Dispositivo para inferência ('cpu' ou 'cuda').
        """
        self.model = model
        self.device = torch.device(device)
        self.model.to(self.device)
        self.model.eval()

    def predict(self, input_data: RecommenderInput) -> float:
        """Realiza a inferência baseada no input validado.

        Args:
            input_data: Objeto validado pelo schema Pydantic.

        Returns:
            O valor da predição convertido para float.
        """
        user = torch.tensor([input_data.user_idx], dtype=torch.long).to(self.device)
        item = torch.tensor([input_data.item_idx], dtype=torch.long).to(self.device)

        with torch.no_grad():
            output = self.model(user, item)
        return float(output.item())

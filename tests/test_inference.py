import pandas as pd
from src.models.predict import Predictor
from src.schema import RecommenderInput


def test_recommender() -> None:
    """Realiza a recomendação de itens baseada em um DataFrame de entrada.

    Args:
        input_data (pd.DataFrame): DataFrame contendo os IDs de visitantes e/ou itens
            a serem processados. Deve seguir o formato validado pelo Schema.

    Returns:
        list: Lista contendo os scores de recomendação ou os IDs dos itens recomendados.

    Raises:
        ValueError: Se o DataFrame de entrada estiver vazio ou fora do formato esperado.
    """
    sample_input = pd.DataFrame(
        {
            "user_idx": [12345],
            "item_idx": [67890],
        }
    )

    print("--- 1. Validando Schema ---")
    try:
        # Validação contra o seu schema.py
        RecommenderInput.validate(sample_input)
        print("Schema OK!")
    except Exception as e:
        print(f"Erro no Schema: {e}")
        return

    print("--- 2. Executando Predição ---")
    try:
        resultado = Predictor(sample_input)
        print(f"Predição gerada com sucesso: {resultado}")
    except Exception as e:
        print(f"Erro na execução do predict: {e}")


if __name__ == "__main__":
    test_recommender()

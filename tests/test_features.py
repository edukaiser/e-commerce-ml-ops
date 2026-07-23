"""Módulo de testes para as etapas de feature engineering."""

import pandas as pd
from src.stages.feature_eng import compute_implicit_feedback


def test_compute_implicit_feedback() -> None:
    """Testa se o cálculo do target ponderado e Min-Max.

    scaling funciona corretamente.
    """
    # Cria um DataFrame de mock simulando dados de entrada
    df_input = pd.DataFrame(
        {
            "user_idx": [1, 1, 2],
            "item_idx": [10, 20, 10],
            "event": ["view", "transaction", "addtocart"],
        }
    )

    df_result = compute_implicit_feedback(df_input)

    # Verifica se a coluna target foi criada
    assert "target" in df_result.columns

    # Verifica se os valores normalizados estão estritamente entre 0.0 e 1.0
    assert df_result["target"].min() >= 0.0
    assert df_result["target"].max() <= 1.0

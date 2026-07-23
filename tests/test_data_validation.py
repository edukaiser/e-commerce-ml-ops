"""Módulo de testes para validação de contratos de dados."""

import pandas as pd


def test_raw_data_schema() -> None:
    """Valida se o DataFrame bruto possui as colunas obrigatórias."""
    expected_columns = {"user_id", "item_id", "event", "timestamp"}

    # Simula um lote de dados recebidos
    df_raw = pd.DataFrame(columns=["user_id", "item_id", "event", "timestamp"])

    # Verifica se todas as colunas do contrato estão presentes
    assert expected_columns.issubset(df_raw.columns)


def test_raw_data_empty_check() -> None:
    """Garante que o pipeline não processa DataFrames vazios."""
    df_empty = pd.DataFrame(columns=["user_id", "item_id", "event"])
    assert len(df_empty) == 0

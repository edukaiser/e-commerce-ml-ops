"""Módulo de Engenharia de Recursos (Feature Engineering).

Este módulo implementa o mapeanto denso de IDs para Embeddings e a 
criação do target adaptativo baseado em implicit feedback para o PyTorch.
"""

import pandas as pd

def create_dense_mappings(df: pd.DataFrame) -> tuple[pd.DataFrame, dict, dict]:
    """Cria mapeamentos sequenciais densos para os IDs de visitantes e itens.
    
    Args:
        df(pd.DataFrame): DataFrame com os dados filtrados do estágio anterior.

    Returns:
        tuple: DataFrame atualizado, dicionário de usuários e dicionário de itens.
    """

    # Gera mapeamentos de 0 até N-1 para evitar eparsidade no PyTorch
    user_mapping = {uid: idx for idx, uid in enumerate(df["visitorid"].unique())}
    item_mapping = {iid: idx for idx, iid in enumerate(df["itemid"].unique())}

    df_mapped = df.copy()
    df_mapped["user_idx"] = df_mapped["visitorid"].map(user_mapping)
    df_mapped["item_idx"] = df_mapped["itemid"].map(item_mapping)

    return df_mapped, user_mapping, item_mapping

def compute_implicit_feedback(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula o target adaptativo ponderado com base nas interações do usuário.
    
    Args:
        df (pd.DataFrame): DataFrame com os IDs mapeados.

    Returns:
        pd.DataFrame: DataFrame com a coluna 'target' calculada.
    """

    # Pesos definidos no plano de ação para mitigar o desbalanceamento critico
    weight_map = {"view": 1.0, "addtocart": 3.0, "transaction": 5.0}

    df_weighted = df.copy()
    df_weighted["interaction_weight"] = df_weighted["event"].map(weight_map)

    # Agrupa por usuário e item somando os pesos das interações
    df_grouped = (
        df_weighted.groupby(["user_idx", "item_idx"])["interaction_weight"]
        .sum()
        .reset_index()
    )

    # Renomeia para 'target' conforme o padrão exigido
    df_grouped = df_grouped.rename(columns={"interaction_weight": "target"})
    return df_grouped

def main() -> None:
    """Função principal para executar o estágio de feature engineering."""
    print("=== Iniciando o estágio de Feature Engineering ===")

    # 1. Carrega o output do estágio anterior
    input_path = "data/interim/events_filtered.csv"
    print(f"Lendo dados filtrados de: {input_path}")
    df_interim = pd.read_csv(input_path)

    # 2. Executa as transformações
    df_mapped, _, _ = create_dense_mappings(df_interim)
    df_features = compute_implicit_feedback(df_mapped)

    print(f"Total de interações densas user-item geradas: {df_features.shape[0]}")

    # 3. Salva o dataset final pronto para o treino da MLP
    output_path = "data/processed/features_ready.csv"
    df_features.to_csv(output_path, index=False)
    print(f"Dados processados salvos com sucesso em: {output_path}")
    print("====== ESTÁGIO FEATURE ENGINEERING CONCLUÍDO ======\n")


if __name__ == "__main__":
    main()
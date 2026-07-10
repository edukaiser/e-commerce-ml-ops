"""Módulo de pré-processamento de dados utilizando o padrão Strategy.

Este módulo aplica os filtros limiares discutidos no EDA para o dataset
do RetailRocket, garantindo código limpo e modular.
"""

from abc import ABC, abstractmethod
import pathlib
import pandas as pd


class PreprocessingStrategy(ABC):
    """Classe abstrata base para as estratégias de filtragem de dados."""

    @abstractmethod
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica o filtro específico no DataFrame.

        Args:
            df (pd.DataFrame): DataFrame original do RetailRocket.

        Returns:
            pd.DataFrame: DataFrame filtrado.
        """
        pass


class FilterGhostUsersStrategy(PreprocessingStrategy):
    """Remove usuários fantasmas com histórico menor que o limiar determinado."""

    def __init__(self, min_interactions: int = 3) -> None:
        """Inicializa a estratégia com o limite mínimo de interações."""
        self.min_interactions = min_interactions

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filtra usuários baseado na volumetria mínima de interações."""
        user_counts = df["visitorid"].value_counts()
        valid_users = user_counts[user_counts >= self.min_interactions].index
        return df[df["visitorid"].isin(valid_users)].copy()


class FilterLongTailItemsStrategy(PreprocessingStrategy):
    """Remove produtos com baixíssima frequência (cauda longa)."""

    def __init__(self, min_appearances: int = 5) -> None:
        """Inicializa a estratégia com o limite mínimo de aparições."""
        self.min_appearances = min_appearances

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filtra itens baseado na frequência mínima de aparições."""
        item_counts = df["itemid"].value_counts()
        valid_items = item_counts[item_counts >= self.min_appearances].index
        return df[df["itemid"].isin(valid_items)].copy()


class DataPreprocessor:
    """Contexto que gerencia e executa as estratégias de pré-processamento."""

    def __init__(self) -> None:
        """Inicializa o contexto com uma lista vazia de estratégias."""
        self._strategies: list[PreprocessingStrategy] = []

    def add_strategy(self, strategy: PreprocessingStrategy) -> None:
        """Adiciona uma nova estratégia de limpeza ao pipeline."""
        self._strategies.append(strategy)

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        """Executa todas as estratégias de pré-processamento no DataFrame."""
        df_processed = df.copy()
        for strategy in self._strategies:
            df_processed = strategy.apply(df_processed)
        return df_processed


def main() -> None:
    """Função principal para executar o estágio de pré-processamento."""
    print("====== INICIANDO ESTÁGIO: PREPROCESS ======")

    # 1. Carrega os dados brutos
    raw_data_path = "data/raw/events.csv"
    print(f"Lendo dados brutos de: {raw_data_path}")
    df_raw = pd.read_csv(raw_data_path)

    # 2. Configura o Preprocessos com as estratégias do edital/EDA
    preprocessor = DataPreprocessor()
    preprocessor.add_strategy(FilterGhostUsersStrategy(min_interactions=3))
    preprocessor.add_strategy(FilterLongTailItemsStrategy(min_appearances=5))

    # 3. Executa a limpeza
    print(f"Volumetria inicial: {df_raw.shape[0]} linhas.")
    df_clean = preprocessor.run(df_raw)
    print(f"Volumetria após filtrados: {df_clean.shape[0]} linhas.")

    # 4. Cria a pasta interim
    output_path = "data/interim/events_filtered.csv"
    pathlib.Path("data/interim").mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(output_path, index=False)
    print(f"Dados salvos com sucesso em: {output_path}")
    print("====== ESTÁGIO PREPROCESS CONCLUÍDO ======\n")


if __name__ == "__main__":
    main()

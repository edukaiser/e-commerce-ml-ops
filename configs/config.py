from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações do projeto carregadas de variáveis de ambiente.

    Atributos:
        MLFLOW_TRACKING_URI (str): URI para o servidor do MLFlow
        DATA_PATH (str): Caminho para o arquivo de dados.
    """

    # Carrega o arquivo .env automaticamente
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    MLFLOW_TRACKING_URI: str = "file:./mlruns"
    DATA_PATH: str = "./data/processed/features_ready.csv"


# Instância única para ser importada no restante do projeto
settings = Settings()

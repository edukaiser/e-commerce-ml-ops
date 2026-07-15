import os
import sys
from pathlib import Path
from dotenv import load_dotenv


def validate_environment() -> None:
    """Valida se o ambiente possui todas as dependências e variáveis necessárias.

    Verifica a existência de pastas essenciais, a presença de variáveis de
    ambiente críticas e a integridade do arquivo de dados para o pipeline.

    Raises:
        SystemExit: Encerra o programa com status 1 caso falte algum item crítico.
    """
    # Carrega o .env automaticamente
    load_dotenv()

    print("--- Iniciando Validação do Ambiente ---")

    # 1. Lista de pastas criticas
    required_dirs = ["data", "models", "configs"]
    for folder in required_dirs:
        if not os.path.exists(folder):
            print(f"ERRO: A pasta {folder} não foi encontrada na raiz.")
            sys.exit(1)

    # 2. Variáveis de ambiente críticas
    critical_vars = ["MLFLOW_TRACKING_URI"]
    missing = [var for var in critical_vars if var not in os.environ]

    if missing:
        print(
            f"AVISO: As seguintes vriáveis de ambiente não foramencontradas: {missing}."
        )
        print("Dica: Certifique-se de que o seu arquivo .env está sendo carregado.")
    else:
        print("SUCESSO: Variáveis de ambiente configuradas")

    # 3. Validação do arquivo de dados
    data_path = Path("data/processed/features_ready.csv")
    if not data_path.exists():
        print(
            "ERRO: Arquivo de treino 'data/processed/features_ready.csv'não encontrado."
        )


print("--- Ambiente Validado com Sucesso! ---")

if __name__ == "__main__":
    validate_environment()

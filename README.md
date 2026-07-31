![Descrição da imagem](docs/img/mlops_banner.png)

# 🛒 E-commerce ML Ops

Projeto de Machine Learning Ops para construção de um sistema de recomendação para e-commerce, com foco em reprodutibilidade, rastreabilidade, experimentação e preparação para deploy de inferência.

Resumo rápido (Vídeo Explicativo):  [Vídeo Resumo do Sistema de Recomendação.](https://drive.google.com/file/d/1PXRWodFOVnCTjV2K_-473FIRNx82r2X_/view?usp=drive_link)

---

## 🎯 Visão Geral

Este repositório organiza um fluxo completo de desenvolvimento de modelos de recomendação, começando com pipelines de dados, treinamento de modelos baseline e rastreamento de experimentos com MLflow. O objetivo é servir como base para evoluir para soluções mais robustas de recomendação, incluindo modelos mais avançados e inferência via API.

---

👥 Integrante: Eduardo Marafigo Kaiser | RM370237

---

## 🏁 Objetivos

- 🔁 Construir um pipeline de ML reproducível;
- 📦 Versionar dados e artefatos de forma controlada;
- 📊 Treinar modelos baseline para comparação;
- 📈 Registrar experimentos e métricas no MLflow;
- 🚀 Preparar a base para deploy e inferência em produção.

---

## 📌 Status do Projeto

- **Estado atual:** MVP inicial com pipeline de treinamento de baselines;
- **Modelo atual:** baselines clássicos de classificação com `scikit-learn`;
- **Componentes em evolução:** pipeline de dados, API de inferência, containerização e CI/CD.

---

## 🏛️ Arquitetura do Projeto

O projeto é organizado em camadas com foco em MLOps:

- 🗄️ **Camada de Dados:** ingestão, limpeza, transformações e versionamento;
- ⚙️ **Camada de Pipeline:** pré-processamento, feature engineering e treinamento;
- 🧠 **Camada de Modelo:** modelos baseline e futuros modelos avançados;
- 🌐 **Camada de Serviço:** inferência via API;
- 🔬 **Camada de Observabilidade:** MLflow, logs, métricas e artefatos.

---

## 🛠️ Stack Tecnológica

- 🐍 Python 3.12
- 🧪 scikit-learn
- 🐼 pandas
- 🔢 numpy
- 🔥 PyTorch *(planejado/estruturado para evolução)*
- ⚡ FastAPI *(para inferência via API)*
- 📊 MLflow
- 📦 DVC
- 🐳 Docker / Docker Compose
- 🧪 pytest
- 🧹 ruff
- 🪝 pre-commit
- ⚡ uv

---

## 📂 Estrutura do Repositório
```text
e-commerce-ml-ops/
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── docs/
│   ├── arquitetura.md
│   └── model_card.md
├── models/
├── notebooks/
├── reports/
├── src/
│   ├── api/
│   ├── models/
│   └── stages/
├── tests/
├── action_plan.md
├── dvc.yaml
├── params.yaml
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 📦 Pré-requisitos
Antes de começar, certifique-se de ter instalado:

Python 3.12

uv

Git

## ⚙️ Configuração do Ambiente
**1. Clone o repositório**

```bash
git clone https://github.com/edukaiser/e-commerce-ml-ops
cd e-commerce-ml-ops
```

**2. Crie e ative um ambiente virtual**

No Linux/macOS:
```bash
uv venv .venv
source .venv/bin/activate
```

No Windows:
```bash
uv venv .venv
.venv\Scripts\activate
```

**3. Instale as dependências**

```bash
uv sync
```

**4. Configure variáveis de ambiente**
Crie um arquivo .env na raiz do projeto com conteúdos como:

Snippet de código
MLFLOW_TRACKING_URI=sqlite:///mlflow.db
🗃️ Dados
Os dados devem ser organizados em:

raw: dados brutos;

interim: dados processados intermediários;

processed: features prontas para treino.

O arquivo esperado pelo pipeline atual é:
data/processed/features_ready.csv

## 🚀 Pipeline Atual

**Treinamento de Baselines**
O script principal de treinamento está localizado em:

src/models/train_and_compare_baselines.py

Ele treina modelos baseline clássicos usando scikit-learn, incluindo:

- Logistic Regression

- Random Forest

- Decision Tree

- KNN

**Como executar**

```bash
uv run python src/models/train_and_compare_baselines.py
```

Esse comando:
carrega os dados processados;

transforma a target em classificação binária;

treina cada baseline;

calcula métricas;

registra os experimentos no MLflow.

## 📊 Rastreamento com MLflow
**O projeto usa MLflow para registrar:**

parâmetros do experimento;

métricas de avaliação;

modelos treinados;

artefatos e logs.

**Iniciar a interface do MLflow:**

```bash
uv run mlflow ui
```

## 🧪 Testes
**Para rodar os testes:**

```bash
uv run pytest
```

## 🧹 Qualidade de Código
**O projeto utiliza:**

```bash
uv run ruff check .
uv run ruff format .
```

E hooks de pre-commit:
```bash
uv run pre-commit install
```

## 📚 Documentação
**A documentação do projeto está organizada em:**

arquitetura.md: descrição da arquitetura proposta;

model_card.md: documentação do modelo e suas limitações;

action_plan.md: plano de evolução do projeto.

## 🤝 Como Contribuir
Faça um fork do projeto;

Crie uma branch para sua feature (git checkout -b feature/sua-feature);

Implemente as mudanças;

Execute testes e checagens;

Abra um pull request.

## 🗺️ Roadmap
**🟢 Curto Prazo**
Consolidar pipeline de dados;

Validar qualidade dos dados;

Expandir o conjunto de métricas;

Estruturar inferência via API.

**🟡 Médio Prazo**
Adicionar modelo de recomendação mais avançado;

Integrar PyTorch ao fluxo;

Versionar artefatos com maior robustez;

Automatizar CI/CD.

**🔵 Longo Prazo**
Deploy em ambiente real;

Monitoramento de performance e drift;

Retraining automatizado;

Escalabilidade para produção.

## 💡 Observações
Este projeto é uma base sólida para evolução em MLOps e recomendação personalizada. Atualmente ele concentra-se em experimentação e estruturação do fluxo, mas já está preparado para crescer em direção a uma solução mais robusta e operacional.

## 📬 Contato
Para dúvidas ou sugestões, utilize o fluxo de issues ou pull requests do repositório.
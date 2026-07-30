# Arquitetura - E-commerce ML Ops

## 1. Visão Geral

Este documento descreve a arquitetura do sistema `e-commerce-ml-ops`, um projeto de Machine Learning Ops voltado para a construção de um pipeline completo de treinamento, avaliação e deployment de um modelo de recomendação para e-commerce.

O sistema foi projetado para:

- gerar recomendações personalizadas de produtos para usuários;
- garantir reprodutibilidade do processo de treinamento;
- versionar dados e artefatos de modelo;
- facilitar o deploy de inferência via API;
- oferecer rastreamento de experimentos e métricas.

---

## 2. Objetivo do Sistema

O projeto tem como objetivo principal implementar uma solução de recomendação baseada em aprendizado profundo, utilizando dados de interação de usuários com produtos, com foco em:

- recomendação personalizada;
- pipeline automatizado de ML;
- rastreamento de experimentos;
- versionamento de dados e modelos;
- deploy simples e escalável de inferência.

A arquitetura foi pensada para ser modular, reproduzível e compatível com boas práticas de MLOps.

---

## 3. Contexto de Negócio

O cenário de negócio é um ambiente de e-commerce onde o usuário interage com produtos por meio de eventos como:

- visualização;
- adição ao carrinho;
- compra.

Esses sinais de interação podem ser usados para inferir preferências e recomendar itens com maior relevância. O modelo implementado usa feedback implícito para aprender padrões de interação entre usuários e produtos.

---

## 4. Princípios de Arquitetura

A arquitetura foi concebida com base nos seguintes princípios:

- Reprodutibilidade: todo o pipeline deve ser executável de forma consistente.
- Versionamento: dados, código, parâmetros e modelos devem ser rastreados.
- Modularidade: cada etapa do pipeline é isolada e substituível.
- Observabilidade: métricas, artefatos e experimentos devem ser acompanhados.
- Portabilidade: o projeto deve ser executável localmente e em containers.
- Manutenibilidade: o código deve seguir boas práticas de organização e testes.

---

## 5. Arquitetura de Alto Nível

```
┌─────────────────────────────────────────────────────────────────┐
│                    E-COMMERCE MLOPS PIPELINE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    CAMADA DE DADOS                        │  │
│  │  Raw Data → Interim Data → Processed Features             │  │   
│  └───────────────────────────────────────────────────────────┘  │
│                                │                                │
│                                ▼                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                 CAMADA DE PIPELINE (DVC)                  │  │
│  │  Preprocess → Feature Engineering → Train → Evaluate      │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                │                                │
│                                ▼                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                  CAMADA DE MODELO                         │  │
│  │    RecommendationMLP (PyTorch) + Artifacts + Metrics      │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                │                                │
│                                ▼                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                  CAMADA DE SERVIÇO                        │  │
│  │      FastAPI → /health → /predict → Recommendations       │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                │                                │
│                                ▼                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │               CAMADA DE OBSERVABILIDADE                   │  │
│  │     MLflow + Logs + Metrics + Evaluation Reports          │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

## 6. Componentes Principais
**6.1 Camada de Dados**
A camada de dados é responsável por armazenar e transformar os dados de interação do usuário.

Estrutura esperada:

raw: dados brutos, geralmente provenientes de fontes externas.
interim: dados filtrados ou limpos após o pré-processamento.
processed: features prontas para treinamento.
Exemplos de dados:

eventos de interação;
identificadores de usuário e item;
tipo de evento;
timestamp.
O processo de versionamento de dados é feito com DVC, permitindo rastrear alterações nos datasets e reexecutar o pipeline de forma consistente.

**6.2 Camada de Pipeline**
O pipeline é organizado em estágios bem definidos, seguindo o fluxo:

Pré-processamento
Engenharia de features
Treinamento
Avaliação
Os arquivos principais desta camada estão localizados em:

preprocess.py
feature_eng.py
train.py
evaluate.py
Esse design favorece a separação de responsabilidades e facilita a evolução do pipeline.

**6.3 Camada de Modelo**
O modelo principal é um modelo de recomendação baseado em redes neurais, implementado com PyTorch.

Características esperadas:

embeddings para usuários e itens;
camadas densas para aprender relações entre embeddings;
saída contínua ou probabilística associada à interação;
treinamento com base em feedback implícito.
O modelo é salvo em artefatos no diretório models, com rastreamento de versão e métricas associadas.

**6.4 Camada de Serviço**
A camada de inferência é exposta por uma API REST utilizando FastAPI.

Principais responsabilidades:

disponibilizar endpoints de saúde;
oferecer inferência de recomendações;
validar entradas com Pydantic;
retornar respostas estruturadas.
Arquivos principais:

main.py
schema.py
predict.py
A API é o ponto de entrada para servir o modelo em ambiente de produção ou teste.

**6.5 Camada de Observabilidade**
A observabilidade do projeto é baseada em:

logs estruturados;
métricas de treinamento;
artefatos de avaliação;
rastreamento de experimentos com MLflow.
Essa camada permite acompanhar:

qual configuração foi usada;
qual modelo foi gerado;
quais métricas foram obtidas;
qual versão de dados alimentou o experimento.

## 7. Fluxo de Execução do Pipeline
**7.1 Fluxo de Dados**
O fluxo de dados segue esta ordem:

Dados brutos são carregados em raw.
O estágio de pré-processamento gera dados limpos em interim.
O estágio de feature engineering transforma os dados em features prontas.
O estágio de treinamento gera um modelo treinado.
O estágio de avaliação gera métricas e artefatos.
A API consome o modelo treinado para inferência.

**7.2 Fluxo de Treinamento**
O ciclo de treinamento é composto por:

definição de parâmetros;
leitura dos dados processados;
construção do modelo;
treinamento com otimizador e função de perda;
avaliação do resultado;
persistência do modelo e métricas.

**7.3 Fluxo de Inferência**
O fluxo de inferência é:

a API recebe uma requisição;
os dados são validados;
o modelo é carregado;
a predição é realizada;
o resultado é retornado em formato JSON.

## 8. Estrutura de Diretórios
```text
e-commerce-ml-ops/
├── .dvc/                     # Configuração do Data Version Control
├── .github/                  # Workflows de CI/CD (quando aplicável)
├── configs/                  # Configurações do projeto
├── data/
│   ├── raw/                  # Dados brutos
│   ├── interim/              # Dados intermediários
│   └── processed/            # Dados prontos para treinamento
├── docs/                     # Documentação
├── models/                   # Artefatos de modelo
├── notebooks/                # EDA e exploração
├── reports/                  # Relatórios e métricas
├── scripts/                  # Scripts utilitários
├── src/
│   ├── api/                  # API FastAPI
│   ├── models/               # Implementação do modelo e predição
│   ├── schema.py             # Schemas Pydantic
│   └── stages/               # Estágios do pipeline
├── tests/                    # Testes unitários e de integração
├── .dockerignore             # Exclusões do Docker
├── .dvcignore                # Exclusões do DVC
├── .gitignore                # Exclusões do Git
├── .pre-commit-config.yaml   # Hooks de qualidade
├── .python-version           # Versão do Python
├── Dockerfile                # Container da aplicação
├── docker-compose.yml        # Orquestração de serviços
├── dvc.lock                  # Lock do pipeline DVC
├── dvc.yaml                  # Definição do pipeline
├── main.py                   # Entry point
├── params.yaml               # Parâmetros do treinamento
├── pyproject.toml            # Configuração do projeto
└── uv.lock                   # Lock de dependências
```

## 9. Tecnologias Utilizadas
O projeto utiliza um stack moderno para apoiar o ciclo de vida completo de ML:

Python 3.12
PyTorch para treinamento do modelo
FastAPI para servindo de inferência
Pydantic para validação de schemas
DVC para versionamento de dados e pipeline
MLflow para rastreamento de experimentos
Docker e Docker Compose para containerização
uv para gerenciamento de dependências
pytest para testes
ruff e pre-commit para qualidade de código

## 10. Decisões de Arquitetura

**10.1 Pipeline Modular**
A divisão em estágios permite separar claramente:

ingestão e limpeza;
engenharia de features;
treinamento;
avaliação;
deployment.
Isso reduz acoplamento e facilita manutenção.

**10.2 Versionamento de Dados e Modelo**
Com DVC e MLflow, o projeto consegue:

rastrear alterações em datasets;
reproduzir experimentos;
associar métricas a versões específicas;
garantir reprodutibilidade do processo.

**10.3 API para Inferência**
A API é um componente separado, permitindo:

servir o modelo independentemente do treinamento;
isolar a lógica de inferência;
facilitar integração com aplicações frontend ou serviços backend.

**10.4 Containerização**
A containerização permite:

execução uniforme em diferentes ambientes;
simplificação do deploy;
isolamento de dependências.

## 11. Requisitos Não Funcionais

A arquitetura foi concebida para atender requisitos importantes de sistemas de ML:

Reprodutibilidade: o mesmo pipeline deve produzir resultados consistentes.
Escalabilidade: a solução pode evoluir para tratar volumes maiores.
Manutenibilidade: o código deve ser organizado e compreensível.
Observabilidade: o sistema deve permitir monitoramento de pipeline e modelo.
Portabilidade: execução local e em container deve ser viável.
Testabilidade: os módulos devem ser facilmente testáveis.

## 12. Segurança e Governança
Algumas boas práticas recomendadas para o projeto incluem:

não armazenar segredos em código;
usar variáveis de ambiente para configurações sensíveis;
controlar acesso aos artefatos do modelo;
registrar versões de modelo e dados de forma auditável;
manter dependências atualizadas e verificadas.

## 13. Pontos de Evolução
A arquitetura atual já é sólida para um MVP/MLOps inicial, mas pode evoluir para cenários mais robustos:

implementação de Feature Store;
pipeline de retraining automatizado;
batch inference para geração periódica de recomendações;
monitoramento online de drift;
integração com CI/CD completo;
deploy em Kubernetes ou serviços cloud;
experimentos com ranking e métricas mais específicas de recomendação.

## 14. Resumo Executivo
A arquitetura do projeto e-commerce-ml-ops organiza o ciclo de vida de um sistema de recomendação em camadas bem definidas:

dados;
pipeline de ML;
treinamento de modelo;
inferência via API;
observabilidade e rastreamento.
Essa estrutura permite desenvolver uma solução de recomendação com foco em reproducibilidade, modularidade, rastreabilidade e escalabilidade, alinhada com boas práticas de MLOps.

## 15. Conclusão
Este projeto representa uma base sólida para um sistema de recomendação em produção, com separação clara entre etapas de dados, treinamento, avaliação e inferência. A arquitetura proposta oferece um caminho natural para evolução, desde um ambiente local e controlado até um cenário mais próximo de produção.
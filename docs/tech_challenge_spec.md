# Tech Challenge — Especificação Técnica

**FIAP Post-Tech — Engenharia de Machine Learning**

Este documento estabelece o guia de arquitetura, governança de código e ciclo de desenvolvimento para o mecanismo de recomendação em e-commerce focado em comportamento de cliques e transações.

---

## 🚀 1. Visão Arquitetural & Core Stack

O objetivo do projeto é construir um motor preditivo robusto alimentado por aprendizado profundo e estruturado sob os pilares modernos da cultura MLOps.

### 📊 Governança do Pipeline e Infraestrutura

* **Abordagem de Modelagem:** Rede Neural baseada em Multilayer Perceptron (MLP) ou camadas dedicadas de *Embeddings*, desenvolvida estritamente via **PyTorch**.
* **Engine de Validação:** Modelos de baseline lineares ou baseados em árvores estruturados via **Scikit-Learn**.
* **Rastreabilidade e Linhagem:** Ciclo de vida de dados controlado de ponta a ponta por **DVC (Data Version Control)**.
* **Orquestração de Experimentos:** Métricas, parâmetros de hiperparametrização e governança de artefatos centralizados no **MLflow Server & Model Registry**.
* **Isolamento de Ambiente:** Containerização multicamadas via **Docker** e composição de microsserviços via **Docker Compose**.

---

## 🛠️ 2. Padrões de Engenharia & Qualidade de Código

### 💻 Governança do Repositório (Git & Dependências)

* **Design Limpo:** Divisão modular estrita usando diretórios dedicados: `src/` (módulos), `tests/` (testes unitários), `data/` (camadas isoladas de dados), `models/` (pesos e checkpoints) e `configs/` (parâmetros de ambiente).
* **Gerenciamento de Escopo:** Divisão explícita de pacotes utilizando `pyproject.toml` (separando estritamente ambientes produtivos de ferramentas de desenvolvimento como `pytest` e `ruff`) com o uso mandatório de arquivos de trava (`uv.lock` / `poetry.lock`).
* **Segurança e Isolamento:** Arquivos sensíveis e temporários blindados via `.gitignore`, `.dockerignore` e definições expostas puramente por arquivos `.env.example`.
* **Versionamento Semântico:** Histórico de commits padronizado para mapear evoluções reais do ecossistema de código.

### 📐 Regras de Ouro de Desenvolvimento (Clean Code)

* **Limitação de Escopo:** Funções altamente coesas e restritas a no máximo 20 linhas de execução.
* **Tipagem Estrita:** Uso mandatório de *Type Hints* em todas as assinaturas de funções públicas acompanhadas de documentação padrão *Google Style*.
* **Padrões de Projeto:** Acoplamento reduzido através da implementação de padrões como *Factory* para inicialização dinâmica de arquiteturas de modelos ou *Strategy* para alternância de algoritmos de pré-processamento.

---

## 📦 3. Matriz de Entregas e Evolução do Projeto

### Fase I: Fundamentos e Linting

* **Objetivo:** Estabelecer a infraestrutura de código estéril e livre de débitos técnicos.
* **Foco Técnico:** Configuração de ganchos automatizados de pré-commit e validação estática via `ruff`.
* **Marco de Entrega:** Repositório estruturado com validação de regras de estilo 100% funcionais.

### Fase II: Determinismo e Ambiente

* **Objetivo:** Garantir o comportamento idêntico do software independente da máquina executora.
* **Foco Técnico:** Centralização de configurações via *Pydantic Settings* e desenvolvimento de rotinas automáticas de diagnóstico ambiental (`validate_env.py`).
* **Marco de Entrega:** Ambiente reprodutível e instalável de forma determinística via comando único.

### Fase III: Versionamento de Dados e Automação de Pipelines

* **Objetivo:** Unificar o rastreio de código ao rastro de dados estruturados.
* **Foco Técnico:** Criação do grafo de execução (`dvc.yaml`) cobrindo uma pipeline com pelo menos três estágios integrados (`preprocess` $\rightarrow$ `feature_eng` $\rightarrow$ `train`). Modelagem de imagens Docker otimizadas utilizando builds de múltiplos estágios (*multi-stage*).
* **Marco de Entrega:** Execução completa do fluxo de ponta a ponta disparado de forma idempotente via CLI do DVC.

### Fase IV: Ciclo de Vida do Modelo e Produção

* **Objetivo:** Treinar, avaliar e governar o ativo preditivo final.
* **Foco Técnico:** Treinamento do estimador PyTorch, validação cruzada contra benchmarks de mercado avaliando um painel de no mínimo 4 métricas distintas, registro no catálogo do MLflow e promoção de estágios (*Staging* para *Production*).
* **Marco de Entrega:** Modelo homologado no *Registry*, geração de documentação de governança (*Model Card*) e fechamento da tese de negócio.

---

## 📐 4. Protocolo de Avaliação (KPIs de Engenharia)

```
[Clean Code e Arquitetura] ── 15% ➔ SOLID, Padrões de Projeto e Linting
[Reprodutibilidade]        ── 15% ➔ Isolamento de Ambiente e Gestão de Deps
[Conteinerização]          ── 15% ➔ Otimização de Dockerfile e Compose
[Linhagem de Dados]        ── 15% ➔ Versionamento e Pipeline DVC (dvc repro)
[Deep Learning Core]       ── 15% ➔ Modelo PyTorch e Análise contra Baselines
[Ciclo de Vida MLOps]      ── 10% ➔ Rastreamento de Runs e Governança de Modelos
[Apresentação Executiva]   ── 10% ➔ Metodologia STAR em Linha do Tempo (5 min)
[Performance Cloud]        ── +5% ➔ (Bônus) Disponibilização de Endpoint Público

```

---

## 💾 5. Estratégia de Dados (Escopo de Entrada)

O ecossistema aceita qualquer repositório de interações comerciais que supere a marca volumétrica mínima de **10.000 eventos** mapeando a relação usuário-item. O benchmark oficial de validação do projeto será executado sobre os dados logados de navegação e consumo do **RetailRocket**, avaliando os comportamentos comportamentais dos usuários.
# Plano de Ação & Arquitetura do Pipeline (Pós-EDA)
**Projeto:** Motor de Recomendação para E-Commerce — RetailRocket  
**Fase:** Transição de Análise Exploratória para Engenharia de Recursos

---

## 🔍 1. Diagnósticos Reais do Dataset (Outputs do EDA)

Com base nas análises executadas no ambiente de experimentação (`notebooks/01_eda.ipynb`), mapeamos as seguintes características mandatórias do ecossistema de dados:

1. **Desbalanceamento Crítico do Funil:** As interações de visualização (`view`) dominam **96.67%** do banco de dados, enquanto intenções claras de compra (`transaction`) representam apenas **0.81%**. 
2. **Alta Volatilidade de Usuários:** Existe um volume massivo de usuários "fantasmas" que possuem apenas 1 interação registrada no histórico, gerando ruído e esparsidade severa para representações vetoriais (*embeddings*).
3. **Dinâmica de Navegação (Sessões Rápidas):** A análise temporal revelou uma mediana de **2.27 minutos** entre cliques consecutivos do mesmo usuário. Isso prova que as jornadas de compra são extremamente imediatas e sequenciais.

---

## 🛠️ 2. Arquitetura Modular do Pipeline (`dvc.yaml`)

Para garantir a reprodutibilidade exigida, o fluxo de dados será governado pelo DVC e dividido em **quatro estágios** independentes e idempotentes, isolados na pasta `src/stages/`:


```

[data/raw] ➔ (preprocess.py) ➔ [data/interim] ➔ (feature_eng.py) ➔ [data/processed] ➔ (train.py) ➔ [models] ➔ (evaluate.py)

```

### 📋 Detalhamento Técnico das Etapas

### Estágio I: `preprocess` (`src/stages/preprocess.py`)
* **Objetivo:** Filtragem de ruído, limpeza de dados órfãos e otimização de memória.
* **Estratégia Pós-EDA:** 
  * Aplicar um ponto de corte (*threshold*) para descartar usuários com histórico menor que 3 interações.
  * Remover produtos com baixíssima frequência (cauda longa com menos de 5 aparições).
  * Salvar o output limpo na pasta `data/interim/events_filtered.csv`.
* **Garantia de Qualidade:** Funções com assinatura de tipos (*Type Hints*) de no máximo 20 linhas e tratamento de exceções para volumetria mínima ($\ge 10.000$ linhas).

### Estágio II: `feature_eng` (`src/stages/feature_eng.py`)
* **Objetivo:** Codificação de variáveis esparsas e estruturação do sinal para o PyTorch.
* **Estratégia Pós-EDA:**
  * **Mapeamento Denso de IDs:** Como as chaves originais do RetailRocket são esparsas, criaremos um dicionário indexador sequencial ($0, 1, 2...$) para alimentar as camadas de `torch.nn.Embedding` de usuários e itens.
  * **Target Adaptativo (Implicit Feedback):** Para contornar o fato de as compras serem apenas 0.81% do dado, criaremos uma matriz de peso ponderado para as interações: `view` = 1.0, `addtocart` = 3.0 e `transaction` = 5.0.
  * Separar os dados em treino, validação e teste usando uma janela de corte temporal (garantindo que o teste avalie apenas o futuro, evitando *data leakage*).
  * Salvar matrizes processadas em `data/processed/`.

### Estágio III: `train` (`src/stages/train.py`)
* **Objetivo:** Inicialização, treinamento e parada antecipada da rede neural.
* **Estratégia Pós-EDA:**
  * Construir a arquitetura **Multi-Layer Perceptron (MLP)** via PyTorch, onde o tamanho das camadas de entrada será exatamente a cardinalidade de usuários e itens únicos mapeados no EDA.
  * Implementação de rotinas de *Early Stopping* baseadas no erro da validação para mitigar o *overfitting*.
  * Acoplamento mandatório do loop de treino com o servidor local do **MLflow** para salvar hiperparâmetros (taxa de aprendizado, tamanho do lote, dropout) e curvas de perda.

### Estágio IV: `evaluate` (`src/stages/evaluate.py`)
* **Objetivo:** Homologação do artefato preditivo e comparação de performance.
* **Estratégia Pós-EDA:**
  * Avaliação do modelo final contra um baseline estático do Scikit-Learn.
  * Geração do painel com as 4 métricas obrigatórias de recomendação (ex: *Precision@K*, *Recall@K*, *NDCG@K* e *F1-Score*).
  * Registro definitivo do modelo aprovado no **MLflow Model Registry** sob a tag `Staging` ou `Production`.

---

## 🚀 3. Próximos Passos Imediatos

1. Criar e versionar o documento `docs/action_plan.md` na branch atual de desenvolvimento.
2. Criar a estrutura física de arquivos em `src/stages/` (`__init__.py`, `preprocess.py`, `feature_eng.py`, `train.py`, `evaluate.py`).
3. Codificar as funções estruturadas de filtragem dentro de `preprocess.py` utilizando o gerenciador `uv`.

## 📐 4. Requisitos de Avaliação e Governança (Atendimento ao Regulamento)

Para garantir o cumprimento integral dos critérios de avaliação do Tech Challenge, o projeto adota os seguintes padrões:

* **Design Patterns:** Será implementado o padrão *Strategy* no módulo de pré-processamento para isolar as regras de filtragem de dados e *Factory* no módulo de treino para a inicialização da rede MLP.
* **Validação de Ambiente:** Uso de `Pydantic Settings` para gerenciar o arquivo `.env` e execução obrigatória do script `scripts/validate_env.py` antes do disparo do pipeline.
* **Containerização Eficiente:** Criação de `Dockerfile` utilizando a estratégia multi-stage (otimizando tamanho de imagem) integrado via `docker-compose.yml` com o servidor do MLflow.
* **Métricas Mandatórias:** O estágio de avaliação comparará a MLP (PyTorch) contra um baseline do Scikit-Learn utilizando no mínimo 4 métricas (Precision@K, Recall@K, NDCG@K e F1-Score).
* **Documentação de Modelo:** Geração do `Model Card` detalhando vieses detectados no desbalanceamento do RetailRocket, além do roteiro do vídeo de 5 minutos estruturado estritamente sob o método STAR (Situation, Task, Action, Result).
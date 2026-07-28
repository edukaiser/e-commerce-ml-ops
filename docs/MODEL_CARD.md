# Model Card - Baselines de Recomendação para E-commerce

## 1. Visão Geral

Este Model Card descreve os modelos baseline treinados para o projeto de recomendação do e-commerce ML Ops.  
O objetivo principal é fornecer uma referência inicial de performance para comparação com modelos mais sofisticados, como abordagens baseadas em redes neurais ou ranking moderno.

O pipeline atual treina modelos clássicos de classificação com base em características simples de usuário e item, registrando métricas em MLflow.

---

## 2. Detalhes do Modelo

- Nome do projeto: e-commerce-ml-ops
- Tipo de modelo: baselines de classificação para recomendação
- Implementação: scikit-learn
- Script de treinamento: `src/models/train_and_compare_baselines.py`
- Experimentos rastreados: MLflow
- Artefatos gerados: modelos, métricas e logs

### Modelos incluídos
- Logistic Regression
- Random Forest
- Decision Tree
- K-Nearest Neighbors (KNN)

---

## 3. Uso Pretendido

Este modelo foi concebido para:

- servir como baseline inicial de recomendação;
- comparar desempenho com modelos mais avançados;
- apoiar experimentação e validação de hipóteses de ML;
- fornecer uma referência simples para o ciclo de MLOps.

### Uso apropriado
- benchmark inicial de modelos;
- experimentos acadêmicos e de laboratório;
- validação de pipeline de treinamento e avaliação.

### Uso inadequado
- uso direto em produção sem validação adicional;
- decisões de negócio críticas sem revisão humana;
- aplicação em outros domínios sem readequação dos dados.

---

## 4. Dados de Treinamento

Os modelos foram treinados com dados processados a partir do arquivo:

- `data/processed/features_ready.csv`

### Features utilizadas
- `user_idx`
- `item_idx`

### Variável alvo
A variável alvo original foi transformada em um problema binário:

- valor 1: quando o score de interação ficou acima da mediana;
- valor 0: quando ficou abaixo ou igual à mediana.

Essa transformação foi usada para criar um problema de classificação simples para servir como baseline.

---

## 5. Procedimento de Treinamento

### Estratégia
- split train/test com 80/20;
- random_state = 42;
- treinamento realizado separadamente para cada modelo baseline;
- métricas registradas automaticamente no MLflow.

### Reprodutibilidade
- os experimentos devem ser executados com os mesmos dados e seed;
- os parâmetros do experimento devem ser versionados;
- o pipeline de treinamento deve ser rastreado via MLflow.

---

## 6. Métricas de Avaliação

As métricas registradas no experimento são:

- Accuracy
- Precision
- Recall
- F1 Score

### Tabela de referência
Os valores abaixo devem ser preenchidos com os resultados reais do experimento executado.

| Modelo              |   Accuracy  |   Precision |   Recall    |  F1 Score   |
|---------------------|-------------|-------------|-------------|-------------|
| Logistic Regression |   0.671     |      0      |      0      |      0      |
| Random Forest       |   0.628     |    0.394    |    0.243    |    0.301    |
| Decision Tree       |   0.578     |    0.362    |    0.372    |    0.367    |
| KNN                 |   0.612     |    0.363    |    0.235    |    0.285    |

---

## 7. Limitações

Este modelo possui limitações importantes:

- usa apenas identificadores de usuário e item;
- não incorpora contexto temporal, comportamento sequencial ou características semânticas de produto;
- a definição binária da target pode não refletir plenamente o valor de negócio real;
- o split simples pode não captar variação temporal ou sazonal;
- o modelo pode sofrer com problemas de cold start;
- não há ainda validação ampla de fairness, estabilidade ou drift.

---

## 8. Fatores e Riscos

### Fatores de risco
- viés de popularidade: modelos simples tendem a favorecer itens mais frequentes;
- falta de diversidade nas recomendações;
- desempenho ruim para usuários ou itens novos;
- interpretação limitada das previsões.

### Impactos potenciais
- recomendações pouco personalizadas;
- reforço de padrões já dominantes no histórico;
- degradação da experiência do usuário em cenários mais complexos.

---

## 9. Considerações Éticas

Antes de usar este modelo em ambiente de produção, recomenda-se avaliar:

- viés de recomendação;
- impacto sobre a diversidade de itens;
- privacidade e proteção de dados;
- transparência das decisões;
- compatibilidade com políticas de uso do negócio.

---

## 10. Recomendações

Para evoluir este projeto, recomenda-se:

- comparar os baselines com um modelo de recomendação mais avançado;
- adicionar features contextuais, como categoria, preço, histórico de sessão e tempo;
- realizar validação temporal e não apenas random split;
- incluir métricas específicas de recomendação, como recall@k e ndcg@k;
- monitorar drift e performance após implantação.

---

## 11. Observações Finais

Este modelo é um ponto de partida sólido para o desenvolvimento de uma solução de recomendação dentro do pipeline MLOps.  
Ele é útil para benchmark, experimentação e validação inicial, mas não deve ser tratado como a versão final de produção sem avaliação adicional e evolução do pipeline.

---

## 12. Versão

- Versão: 0.1
- Status: draft / baseline
- Última atualização:  23/07/2026          
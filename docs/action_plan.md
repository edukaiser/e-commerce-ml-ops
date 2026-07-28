# Action Plan - E-commerce ML Ops

## 1. Objetivo

Construir um ciclo completo de Machine Learning Ops para um sistema de recomendação de produtos, cobrindo desde a preparação dos dados até o deploy da inferência em API, com foco em reprodutibilidade, rastreabilidade e qualidade.

---

## 2. Escopo do Projeto

O projeto deve evoluir para um fluxo completo de ML, incluindo:

- ingestão e versionamento de dados;
- pipeline de pré-processamento e feature engineering;
- treinamento e avaliação de modelos;
- rastreamento de experimentos;
- deploy de inferência via API;
- testes automatizados;
- containerização e automação de CI/CD.

---

## 3. Diretrizes Principais

O plano deve seguir os seguintes princípios:

- Reprodutibilidade: todos os passos devem ser executáveis de forma consistente.
- Versionamento: dados, código, parâmetros e modelos devem ser rastreados.
- Automação: pipelines e validações devem rodar sem intervenção manual.
- Observabilidade: métricas, logs e artefatos devem ser acompanhados.
- Qualidade: testes, linting e validações devem fazer parte do fluxo.

---

## 4. Fases do Plano

### Fase 0 - Fundação do Projeto

Objetivo: estruturar a base do repositório para crescer com qualidade.

Atividades:

- [ ] padronizar a estrutura de diretórios;
- [ ] definir ambiente de execução com `uv` ou `pip-tools`;
- [ ] configurar `ruff`, `pytest` e `pre-commit`;
- [ ] criar documentação inicial (`README`, `docs/`);
- [ ] definir convenções de código e organização de módulos;
- [ ] definir contratos de entrada e saída de dados.

Entregáveis:

- projeto com estrutura organizada;
- ambiente reproduzível;
- qualidade mínima de código garantida.

---

### Fase 1 - Pipeline de Dados

Objetivo: transformar dados brutos em dados prontos para treinamento.

Atividades:

- [ ] definir schema dos dados brutos;
- [ ] implementar ingestão e validação inicial;
- [ ] criar pipeline de limpeza e normalização;
- [ ] implementar engenharia de features;
- [ ] separar dados em `raw`, `interim` e `processed`;
- [ ] versionar datasets com `DVC`;
- [ ] registrar metadados e qualidade dos dados.

Entregáveis:

- dataset processado e versionado;
- pipeline de dados reproduzível;
- artefatos intermediários rastreados.

---

### Fase 2 - Treinamento e Experimentação

Objetivo: treinar modelos de forma controlada e rastreável.

Atividades:

- [ ] implementar script de treinamento;
- [ ] externalizar hiperparâmetros em `params.yaml`;
- [ ] configurar seeds para reprodutibilidade;
- [ ] salvar modelo e artefatos em `models/`;
- [ ] registrar métricas e experimentos com `MLflow`;
- [ ] comparar versões de modelo;
- [ ] definir critérios de aceitação para o modelo.

Entregáveis:

- modelo treinado com artefatos persistidos;
- experimentos registrados;
- métricas comparáveis entre execuções.

---

### Fase 3 - Inferência e API

Objetivo: disponibilizar recomendações por meio de uma API.

Atividades:

- [ ] implementar endpoint de saúde (`/health`);
- [ ] implementar endpoint de predição (`/predict`);
- [ ] carregar o modelo treinado de forma robusta;
- [ ] validar entradas com `Pydantic`;
- [ ] retornar respostas estruturadas em JSON;
- [ ] adicionar testes de API;
- [ ] garantir compatibilidade com o modelo salvo.

Entregáveis:

- API funcional;
- inferência pronta para uso;
- cobertura básica de testes.

---

### Fase 4 - Containerização e Automação

Objetivo: tornar o projeto executável em diferentes ambientes com automação.

Atividades:

- [ ] criar `Dockerfile`;
- [ ] configurar `docker-compose.yml`;
- [ ] criar workflow de CI com `pytest`, `ruff` e build;
- [ ] validar pipeline completo em container;
- [ ] automatizar execução de testes em PRs;
- [ ] preparar ambiente para deploy futuro.

Entregáveis:

- aplicação rodando em container;
- pipeline de validação automatizado;
- processo de integração contínua funcional.

---

### Fase 5 - Observabilidade e Evolução

Objetivo: preparar o projeto para operação e evolução contínua.

Atividades:

- [ ] implementar logs estruturados;
- [ ] monitorar latência e erros da API;
- [ ] registrar métricas de uso e performance;
- [ ] planejar retraining periódico;
- [ ] avaliar drift de dados e de desempenho;
- [ ] evoluir para batch inference ou serviço mais robusto no futuro.

Entregáveis:

- sistema com observabilidade mínima;
- base para monitoramento e melhoria contínua.

---

## 5. Priorização Recomendada

A ordem ideal de execução é:

1. estrutura do projeto e qualidade de código;
2. pipeline de dados e versionamento;
3. treinamento e experimentos;
4. API de inferência;
5. containerização e CI/CD;
6. observabilidade e evolução.

---

## 6. Critérios de Conclusão de Cada Fase

### Fase 0
- projeto organizado;
- ambiente reproduzível;
- testes e lint configurados.

### Fase 1
- dados limpos e processados;
- dados versionados;
- pipeline executável.

### Fase 2
- modelo treinado;
- métricas registradas;
- experimentos rastreados.

### Fase 3
- API disponível;
- predição funcionando;
- testes automatizados.

### Fase 4
- projeto rodando em container;
- CI funcionando.

### Fase 5
- logs e métricas observáveis;
- estratégia de evolução definida.

---

## 7. Riscos e Mitigações

- Dados inconsistentes:
  - mitigar com validação de schema e testes de qualidade.

- Ambientes diferentes:
  - mitigar com `uv`/`lockfile` e containerização.

- Modelo pouco confiável:
  - mitigar com avaliação rigorosa e experimentos comparativos.

- Deploy manual e frágil:
  - mitigar com CI/CD e automação.

---

## 8. Próximos Passos Imediatos

1. consolidar estrutura do projeto;
2. implementar pipeline de dados;
3. criar treino e avaliação;
4. expor inferência via API;
5. adicionar testes e containerização.

---

## 9. Resumo

Este plano transforma o projeto em uma solução de MLOps mais madura, com foco em:

- dados versionados;
- pipeline automatizado;
- treinamento reproduzível;
- rastreamento de experimentos;
- serving via API;
- qualidade e automação contínua.

Se quiser, eu também posso te entregar uma versão deste `action_plan.md` em formato de roadmap com cronograma semanal ou por sprint.<!-- filepath: c:\dev\Hands-ON - Projetos - TechChallenge\TechChallenge\Fase 2\e-commerce-ml-ops\action_plan.md -->

# Action Plan - E-commerce ML Ops

## 1. Objetivo

Construir um ciclo completo de Machine Learning Ops para um sistema de recomendação de produtos, cobrindo desde a preparação dos dados até o deploy da inferência em API, com foco em reprodutibilidade, rastreabilidade e qualidade.

---

## 2. Escopo do Projeto

O projeto deve evoluir para um fluxo completo de ML, incluindo:

- ingestão e versionamento de dados;
- pipeline de pré-processamento e feature engineering;
- treinamento e avaliação de modelos;
- rastreamento de experimentos;
- deploy de inferência via API;
- testes automatizados;
- containerização e automação de CI/CD.

---

## 3. Diretrizes Principais

O plano deve seguir os seguintes princípios:

- Reprodutibilidade: todos os passos devem ser executáveis de forma consistente.
- Versionamento: dados, código, parâmetros e modelos devem ser rastreados.
- Automação: pipelines e validações devem rodar sem intervenção manual.
- Observabilidade: métricas, logs e artefatos devem ser acompanhados.
- Qualidade: testes, linting e validações devem fazer parte do fluxo.

---

## 4. Fases do Plano

### Fase 0 - Fundação do Projeto

Objetivo: estruturar a base do repositório para crescer com qualidade.

Atividades:

- [ ] padronizar a estrutura de diretórios;
- [ ] definir ambiente de execução com `uv` ou `pip-tools`;
- [ ] configurar `ruff`, `pytest` e `pre-commit`;
- [ ] criar documentação inicial (`README`, `docs/`);
- [ ] definir convenções de código e organização de módulos;
- [ ] definir contratos de entrada e saída de dados.

Entregáveis:

- projeto com estrutura organizada;
- ambiente reproduzível;
- qualidade mínima de código garantida.

---

### Fase 1 - Pipeline de Dados

Objetivo: transformar dados brutos em dados prontos para treinamento.

Atividades:

- [ ] definir schema dos dados brutos;
- [ ] implementar ingestão e validação inicial;
- [ ] criar pipeline de limpeza e normalização;
- [ ] implementar engenharia de features;
- [ ] separar dados em `raw`, `interim` e `processed`;
- [ ] versionar datasets com `DVC`;
- [ ] registrar metadados e qualidade dos dados.

Entregáveis:

- dataset processado e versionado;
- pipeline de dados reproduzível;
- artefatos intermediários rastreados.

---

### Fase 2 - Treinamento e Experimentação

Objetivo: treinar modelos de forma controlada e rastreável.

Atividades:

- [ ] implementar script de treinamento;
- [ ] externalizar hiperparâmetros em `params.yaml`;
- [ ] configurar seeds para reprodutibilidade;
- [ ] salvar modelo e artefatos em `models/`;
- [ ] registrar métricas e experimentos com `MLflow`;
- [ ] comparar versões de modelo;
- [ ] definir critérios de aceitação para o modelo.

Entregáveis:

- modelo treinado com artefatos persistidos;
- experimentos registrados;
- métricas comparáveis entre execuções.

---

### Fase 3 - Inferência e API

Objetivo: disponibilizar recomendações por meio de uma API.

Atividades:

- [ ] implementar endpoint de saúde (`/health`);
- [ ] implementar endpoint de predição (`/predict`);
- [ ] carregar o modelo treinado de forma robusta;
- [ ] validar entradas com `Pydantic`;
- [ ] retornar respostas estruturadas em JSON;
- [ ] adicionar testes de API;
- [ ] garantir compatibilidade com o modelo salvo.

Entregáveis:

- API funcional;
- inferência pronta para uso;
- cobertura básica de testes.

---

### Fase 4 - Containerização e Automação

Objetivo: tornar o projeto executável em diferentes ambientes com automação.

Atividades:

- [ ] criar `Dockerfile`;
- [ ] configurar `docker-compose.yml`;
- [ ] criar workflow de CI com `pytest`, `ruff` e build;
- [ ] validar pipeline completo em container;
- [ ] automatizar execução de testes em PRs;
- [ ] preparar ambiente para deploy futuro.

Entregáveis:

- aplicação rodando em container;
- pipeline de validação automatizado;
- processo de integração contínua funcional.

---

### Fase 5 - Observabilidade e Evolução

Objetivo: preparar o projeto para operação e evolução contínua.

Atividades:

- [ ] implementar logs estruturados;
- [ ] monitorar latência e erros da API;
- [ ] registrar métricas de uso e performance;
- [ ] planejar retraining periódico;
- [ ] avaliar drift de dados e de desempenho;
- [ ] evoluir para batch inference ou serviço mais robusto no futuro.

Entregáveis:

- sistema com observabilidade mínima;
- base para monitoramento e melhoria contínua.

---

## 5. Priorização Recomendada

A ordem ideal de execução é:

1. estrutura do projeto e qualidade de código;
2. pipeline de dados e versionamento;
3. treinamento e experimentos;
4. API de inferência;
5. containerização e CI/CD;
6. observabilidade e evolução.

---

## 6. Critérios de Conclusão de Cada Fase

### Fase 0
- projeto organizado;
- ambiente reproduzível;
- testes e lint configurados.

### Fase 1
- dados limpos e processados;
- dados versionados;
- pipeline executável.

### Fase 2
- modelo treinado;
- métricas registradas;
- experimentos rastreados.

### Fase 3
- API disponível;
- predição funcionando;
- testes automatizados.

### Fase 4
- projeto rodando em container;
- CI funcionando.

### Fase 5
- logs e métricas observáveis;
- estratégia de evolução definida.

---

## 7. Riscos e Mitigações

- Dados inconsistentes:
  - mitigar com validação de schema e testes de qualidade.

- Ambientes diferentes:
  - mitigar com `uv`/`lockfile` e containerização.

- Modelo pouco confiável:
  - mitigar com avaliação rigorosa e experimentos comparativos.

- Deploy manual e frágil:
  - mitigar com CI/CD e automação.

---

## 8. Próximos Passos Imediatos

1. consolidar estrutura do projeto;
2. implementar pipeline de dados;
3. criar treino e avaliação;
4. expor inferência via API;
5. adicionar testes e containerização.

---

## 9. Resumo

Este plano transforma o projeto em uma solução de MLOps mais madura, com foco em:

- dados versionados;
- pipeline automatizado;
- treinamento reproduzível;
- rastreamento de experimentos;
- serving via API;
- qualidade e automação contínua.
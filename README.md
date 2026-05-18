# BeautyFlow AI

**BeautyFlow AI** é um MVP de aplicativo inteligente para salões de beleza, clínicas de estética, barbearias e profissionais autônomos da área da beleza.

O objetivo do projeto é unir **gestão de agendamentos**, **dashboard de vendas**, **assistente com LLM**, **IA generativa**, **RAG simples** e **recomendação de serviços com Machine Learning** em uma base pronta para evoluir aos poucos.

> Projeto criado para portfólio, estudos e evolução profissional em Python, IA generativa, LLMs, Machine Learning e desenvolvimento de aplicações.

---

## Problema que o BeautyFlow AI resolve

Negócios de beleza normalmente precisam lidar com:

- Falta de organização em agendamentos.
- Clientes que não retornam depois do primeiro atendimento.
- Horários vazios durante a semana.
- Baixa personalização nas mensagens para clientes.
- Dificuldade em analisar faturamento, ticket médio e serviços mais vendidos.
- Pouco uso de dados para recomendar serviços e criar campanhas.

O **BeautyFlow AI** nasce como uma solução para transformar esses dados em decisões mais inteligentes.

---

## Funcionalidades já implementadas

- Backend com **FastAPI**.
- Frontend com **Streamlit**.
- Banco local **SQLite** usando SQLModel.
- Cadastro e listagem de clientes.
- Cadastro e listagem de serviços.
- Cadastro e listagem de profissionais.
- Criação de agendamentos via API.
- Atualização de status de agendamentos.
- Dashboard com métricas do negócio.
- Receita estimada.
- Ticket médio.
- Taxa de no-show.
- Serviços mais agendados.
- Assistente IA para gestão e atendimento.
- Geração de mensagens para WhatsApp.
- Geração de posts de marketing.
- Recomendador de serviços usando **TF-IDF + similaridade de cosseno**.
- RAG simples com base de conhecimento local.
- Modo fallback sem chave de IA, para testar mesmo sem API externa.

---

## Tecnologias utilizadas

- Python 3.11+
- FastAPI
- Streamlit
- SQLModel
- SQLite
- Pandas
- Scikit-learn
- OpenAI SDK opcional
- RAG simples com arquivos locais
- Machine Learning com TF-IDF

---

## Estrutura do projeto

```text
beautyflow_ai/
  app/
    api/
      routes.py
    core/
      config.py
    db/
      database.py
      models.py
    ml/
      recommender.py
    schemas/
      schemas.py
    services/
      ai_service.py
      analytics_service.py
      rag_service.py
    main.py
  data/
    sample_data.py
  frontend/
    streamlit_app.py
  knowledge_base/
    beleza.txt
  .env.example
  .gitignore
  PROJECT_ROADMAP.md
  requirements.txt
  seed.py
```

---

## Como rodar o projeto

### 1. Entre na pasta do projeto

```bash
cd beautyflow_ai
```

### 2. Crie o ambiente virtual

```bash
python -m venv .venv
```

### 3. Ative o ambiente virtual

No Windows:

```bash
.venv\Scripts\activate
```

No Linux ou Mac:

```bash
source .venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env`.

No Windows, você pode copiar manualmente.

No Linux/Mac:

```bash
cp .env.example .env
```

O arquivo `.env.example` já vem assim:

```env
APP_NAME=BeautyFlow AI
DATABASE_URL=sqlite:///beautyflow_ai.db
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
```

Sem `OPENAI_API_KEY`, o app funciona com respostas simuladas. Com a chave configurada, ele passa a usar LLM real.

### 6. Crie o banco com dados iniciais

```bash
python seed.py
```

### 7. Rode o backend

```bash
uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Documentação automática:

```text
http://127.0.0.1:8000/docs
```

### 8. Rode o frontend

Abra outro terminal, ative o ambiente virtual novamente e execute:

```bash
streamlit run frontend/streamlit_app.py
```

---

## O que testar primeiro

1. Abra o frontend no Streamlit.
2. Veja o dashboard inicial.
3. Teste o assistente IA.
4. Gere uma mensagem para WhatsApp.
5. Gere um post de marketing.
6. Descreva uma cliente no recomendador e veja os serviços sugeridos.
7. Abra `http://127.0.0.1:8000/docs` para testar a API.

---

## Diferenciais para portfólio

Este projeto mostra domínio em:

- Desenvolvimento backend com Python.
- Criação de API REST com FastAPI.
- Interface rápida com Streamlit.
- Banco de dados relacional.
- Machine Learning aplicado a recomendação.
- Uso de LLM e IA generativa.
- Estrutura de RAG com base local.
- Pensamento de produto para um nicho real.
- Organização de projeto para GitHub.

---

## Próximos passos recomendados

Para deixar o **BeautyFlow AI** ainda mais profissional:

1. Adicionar tela de login.
2. Criar diferentes perfis: administrador, profissional e recepção.
3. Trocar SQLite por PostgreSQL.
4. Criar deploy da API.
5. Criar deploy do frontend.
6. Integrar WhatsApp Cloud API.
7. Criar previsão de no-show com Machine Learning.
8. Criar segmentação de clientes inativos.
9. Criar análise de fotos com IA, sempre com consentimento.
10. Criar app mobile com React Native ou Flutter.
11. Criar dashboard em Power BI conectado ao banco.
12. Adicionar pagamentos com Mercado Pago ou Stripe.

---

## Sugestão de descrição para GitHub

```text
BeautyFlow AI é um MVP de aplicativo inteligente para negócios da beleza, criado com Python, FastAPI, Streamlit, LLM, IA generativa, RAG e Machine Learning para gestão, atendimento, marketing e recomendação de serviços.
```

---

## Aviso importante

Este projeto é uma base educacional/profissional. Para uso real com clientes, implemente autenticação, criptografia adequada, política de privacidade, controle de permissões, logs, backup, consentimento para dados pessoais e termos de uso.

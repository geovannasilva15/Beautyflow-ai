<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=ec4899&height=180&section=header&text=BeautyFlow%20AI&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=34&desc=Intelig%C3%AAncia%20aplicada%20%C3%A0%20gest%C3%A3o%20de%20beleza&descAlignY=57" alt="BeautyFlow AI" />

</div>

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](#)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](#)

**Protótipo de gestão para salões e clínicas, com agenda, relacionamento com clientes, análises e recursos inteligentes.**

</div>

## Funcionalidades

- Gestão de clientes, serviços e agenda
- Dashboard com indicadores
- Recomendação de serviços
- Assistente para apoio ao atendimento
- Base de conhecimento e recuperação de informações
- API com documentação interativa
- Persistência local com SQLite

## Tecnologias

Python, FastAPI, Streamlit, SQLModel, SQLite, Pandas, scikit-learn, OpenAI SDK e Requests.

## Executar localmente

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python seed.py
python -m uvicorn app.main:app --reload
```

Em outro terminal:

```bash
python -m streamlit run frontend/streamlit_app.py
```

## Arquitetura

```mermaid
flowchart LR
    UI[Interface] --> API[API FastAPI]
    API --> DB[(SQLite)]
    API --> REC[Recomendação]
    API --> KB[Base de conhecimento]
```

## Observação

Este repositório registra uma versão de desenvolvimento do BeautyFlow AI. Credenciais e integrações externas devem ser configuradas por variáveis de ambiente e nunca adicionadas ao código.

## Autoria

Desenvolvido por **[Geovanna Eduarda da Silva](https://github.com/geovannasilva15)**.

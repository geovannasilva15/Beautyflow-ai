from __future__ import annotations

from datetime import datetime, time, timedelta
from typing import Any

import pandas as pd
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/api"

st.set_page_config(
    page_title="BeautyFlow AI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------------------------------------------------------------
# Visual / CSS
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(236, 72, 153, 0.14), transparent 32%),
                radial-gradient(circle at top right, rgba(168, 85, 247, 0.12), transparent 30%),
                linear-gradient(180deg, #fff7fb 0%, #ffffff 36%, #fbf7ff 100%);
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #201126 0%, #321436 54%, #4a1846 100%);
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        section[data-testid="stSidebar"] * {
            color: #fff !important;
        }

        div[data-testid="stSidebarUserContent"] {
            padding-top: 1.4rem;
        }

        .sidebar-logo {
            padding: 18px 16px;
            border-radius: 24px;
            background: rgba(255,255,255,0.10);
            border: 1px solid rgba(255,255,255,0.16);
            box-shadow: 0 16px 45px rgba(0,0,0,0.18);
            margin-bottom: 18px;
        }

        .sidebar-logo h2 {
            margin: 0;
            font-size: 1.35rem;
            letter-spacing: -0.04em;
        }

        .sidebar-logo p {
            margin: 6px 0 0 0;
            color: rgba(255,255,255,0.72) !important;
            font-size: 0.82rem;
        }

        .hero {
            position: relative;
            overflow: hidden;
            padding: 34px 34px;
            border-radius: 34px;
            background:
                linear-gradient(135deg, rgba(255,255,255,0.92), rgba(255,245,251,0.78)),
                linear-gradient(135deg, #fb7185, #d946ef 44%, #7c3aed 100%);
            border: 1px solid rgba(236, 72, 153, 0.16);
            box-shadow: 0 24px 80px rgba(124, 58, 237, 0.14);
            margin-bottom: 24px;
        }

        .hero::after {
            content: "";
            position: absolute;
            right: -90px;
            top: -80px;
            width: 270px;
            height: 270px;
            background: radial-gradient(circle, rgba(236,72,153,0.30), transparent 66%);
            border-radius: 999px;
        }

        .hero-kicker {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            border-radius: 999px;
            background: rgba(236, 72, 153, 0.10);
            color: #be185d;
            font-weight: 700;
            font-size: 0.82rem;
            margin-bottom: 14px;
        }

        .hero h1 {
            margin: 0;
            font-size: clamp(2.3rem, 5vw, 4.8rem);
            line-height: 0.95;
            letter-spacing: -0.07em;
            color: #241126;
        }

        .hero h1 span {
            background: linear-gradient(135deg, #be185d, #9333ea, #4f46e5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero p {
            max-width: 780px;
            margin: 18px 0 0 0;
            color: #6b566f;
            font-size: 1.05rem;
            line-height: 1.65;
        }

        .hero-actions {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 20px;
        }

        .pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 9px 13px;
            border-radius: 999px;
            background: white;
            border: 1px solid rgba(236, 72, 153, 0.16);
            color: #5b315e;
            font-weight: 700;
            font-size: 0.84rem;
            box-shadow: 0 8px 24px rgba(236,72,153,0.10);
        }

        .section-title {
            margin: 8px 0 16px 0;
        }

        .section-title h2 {
            margin-bottom: 4px;
            letter-spacing: -0.04em;
            color: #241126;
        }

        .section-title p {
            margin-top: 0;
            color: #7b657d;
        }

        .metric-card {
            padding: 22px 22px;
            border-radius: 26px;
            background: rgba(255,255,255,0.84);
            border: 1px solid rgba(236, 72, 153, 0.12);
            box-shadow: 0 18px 55px rgba(124,58,237,0.08);
            min-height: 132px;
        }

        .metric-card .label {
            color: #826a84;
            font-size: 0.86rem;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .metric-card .value {
            color: #271129;
            font-size: 2rem;
            font-weight: 850;
            letter-spacing: -0.05em;
            line-height: 1;
        }

        .metric-card .hint {
            color: #a05c89;
            font-size: 0.78rem;
            font-weight: 700;
            margin-top: 12px;
        }

        .glass-card {
            padding: 24px;
            border-radius: 28px;
            background: rgba(255,255,255,0.82);
            border: 1px solid rgba(236, 72, 153, 0.12);
            box-shadow: 0 18px 55px rgba(124,58,237,0.08);
            margin-bottom: 16px;
        }

        .feature-card {
            padding: 22px;
            border-radius: 28px;
            background: linear-gradient(180deg, rgba(255,255,255,0.92), rgba(255,248,252,0.84));
            border: 1px solid rgba(236, 72, 153, 0.14);
            box-shadow: 0 18px 55px rgba(124,58,237,0.08);
            min-height: 210px;
        }

        .feature-card h3 {
            margin: 0 0 8px 0;
            color: #271129;
            letter-spacing: -0.03em;
        }

        .feature-card p {
            color: #745a78;
            line-height: 1.55;
        }

        .tag {
            display: inline-block;
            padding: 6px 10px;
            border-radius: 999px;
            background: #fce7f3;
            color: #be185d;
            font-size: 0.75rem;
            font-weight: 800;
            margin: 4px 4px 0 0;
        }

        .success-badge {
            display: inline-flex;
            gap: 8px;
            align-items: center;
            padding: 8px 12px;
            border-radius: 999px;
            background: rgba(16, 185, 129, 0.12);
            color: #047857;
            font-weight: 800;
            font-size: 0.80rem;
        }

        .danger-badge {
            display: inline-flex;
            gap: 8px;
            align-items: center;
            padding: 8px 12px;
            border-radius: 999px;
            background: rgba(239, 68, 68, 0.12);
            color: #b91c1c;
            font-weight: 800;
            font-size: 0.80rem;
        }

        .mini-caption {
            color: #8a738c;
            font-size: 0.86rem;
            margin-top: -6px;
            margin-bottom: 16px;
        }

        .stButton > button {
            border-radius: 999px !important;
            border: 0 !important;
            padding: 0.65rem 1.05rem !important;
            background: linear-gradient(135deg, #ec4899, #9333ea) !important;
            color: white !important;
            font-weight: 800 !important;
            box-shadow: 0 12px 32px rgba(236, 72, 153, 0.25);
        }

        .stButton > button:hover {
            filter: brightness(1.04);
            transform: translateY(-1px);
        }

        div[data-testid="stMetric"] {
            padding: 18px;
            background: rgba(255,255,255,0.72);
            border-radius: 24px;
            border: 1px solid rgba(236, 72, 153, 0.10);
        }

        div[data-testid="stExpander"] {
            border-radius: 22px !important;
            border: 1px solid rgba(236, 72, 153, 0.12) !important;
            overflow: hidden;
            background: rgba(255,255,255,0.78);
        }

        .footer-note {
            margin-top: 30px;
            padding: 16px 18px;
            border-radius: 20px;
            background: rgba(255,255,255,0.72);
            color: #7b657d;
            border: 1px solid rgba(236, 72, 153, 0.10);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# API helpers
# -----------------------------------------------------------------------------
def api_get(path: str) -> Any:
    response = requests.get(f"{API_URL}{path}", timeout=20)
    response.raise_for_status()
    return response.json()


def api_post(path: str, json: dict | None = None, params: dict | None = None) -> Any:
    response = requests.post(f"{API_URL}{path}", json=json, params=params, timeout=60)
    response.raise_for_status()
    return response.json()


def format_currency(value: float | int | None) -> str:
    value = float(value or 0)
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def section_title(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="section-title">
            <h2>{title}</h2>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, hint: str, icon: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="label">{icon} {label}</div>
            <div class="value">{value}</div>
            <div class="hint">{hint}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">✨ SaaS inteligente para beleza, estética e bem-estar</div>
            <h1>BeautyFlow <span>AI</span></h1>
            <p>
                Gestão visual para negócios de beleza com dashboard, assistente LLM, recomendação inteligente,
                cadastro de clientes, serviços e geração de campanhas. Um MVP com cara de produto real para evoluir
                no portfólio.
            </p>
            <div class="hero-actions">
                <span class="pill">💄 Beleza</span>
                <span class="pill">🤖 IA generativa</span>
                <span class="pill">🧠 Machine Learning</span>
                <span class="pill">🐍 Python + FastAPI</span>
                <span class="pill">📊 Dashboard</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def safe_dataframe(data: list[dict] | pd.DataFrame, empty_message: str) -> pd.DataFrame:
    df = pd.DataFrame(data)
    if df.empty:
        st.info(empty_message)
    return df


def api_status_badge() -> bool:
    try:
        api_get("/health")
        st.sidebar.markdown('<span class="success-badge">● API conectada</span>', unsafe_allow_html=True)
        return True
    except Exception:
        st.sidebar.markdown('<span class="danger-badge">● API offline</span>', unsafe_allow_html=True)
        return False


# -----------------------------------------------------------------------------
# Sidebar
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-logo">
            <h2>💎 BeautyFlow AI</h2>
            <p>Dashboard, IA e automação para negócios de beleza.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Menu principal",
        [
            "Início",
            "Dashboard",
            "Agenda",
            "Assistente IA",
            "Recomendador",
            "Clientes",
            "Serviços",
            "Marketing IA",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    online = api_status_badge()
    st.caption("Frontend: Streamlit")
    st.caption("Backend: FastAPI")
    st.caption("API: http://127.0.0.1:8000/docs")

if not online:
    hero()
    st.error("API não encontrada. Abra outro terminal e rode: python -m uvicorn app.main:app --reload")
    st.stop()


# -----------------------------------------------------------------------------
# Pages
# -----------------------------------------------------------------------------
if page == "Início":
    hero()
    section_title("Central inteligente do negócio", "Uma visão mais bonita, comercial e profissional para apresentar no GitHub, LinkedIn e portfólio.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <h3>📊 Gestão visual</h3>
                <p>Cards, indicadores e gráficos para acompanhar receita, clientes, agendamentos, ticket médio e no-show.</p>
                <span class="tag">Dashboard</span><span class="tag">Métricas</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <h3>🤖 Assistente LLM</h3>
                <p>IA para responder perguntas de gestão, criar mensagens de WhatsApp e apoiar estratégias de relacionamento.</p>
                <span class="tag">LLM</span><span class="tag">IA generativa</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <h3>🧠 Recomendações</h3>
                <p>Modelo simples de recomendação para sugerir serviços com base no perfil, objetivo e interesses da cliente.</p>
                <span class="tag">Machine Learning</span><span class="tag">Python</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="footer-note">
            Próxima evolução recomendada: login, tela pública de agendamento, integração com WhatsApp, pagamentos e deploy.
        </div>
        """,
        unsafe_allow_html=True,
    )

elif page == "Dashboard":
    hero()
    section_title("Dashboard executivo", "Acompanhe a saúde do negócio com indicadores rápidos e gráficos limpos.")

    data = api_get("/dashboard")
    appointments = safe_dataframe(api_get("/appointments"), "Ainda não existem agendamentos cadastrados.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Clientes", str(data["total_clients"]), "Base cadastrada", "👥")
    with col2:
        metric_card("Agendamentos", str(data["total_appointments"]), "Histórico total", "📅")
    with col3:
        metric_card("Receita estimada", format_currency(data["estimated_revenue"]), "Serviços concluídos", "💰")
    with col4:
        metric_card("Ticket médio", format_currency(data["average_ticket"]), "Valor por atendimento", "💎")

    st.write("")
    col5, col6, col7 = st.columns(3)
    with col5:
        st.metric("Concluídos", data["completed_appointments"], help="Atendimentos finalizados")
    with col6:
        st.metric("Marcados", data["scheduled_appointments"], help="Agendamentos futuros ou pendentes")
    with col7:
        st.metric("Taxa de no-show", f"{data['no_show_rate'] * 100:.1f}%", help="Clientes que não compareceram")

    chart_col, table_col = st.columns([1.2, 1])
    with chart_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Serviços mais agendados")
        top_services = pd.DataFrame(data["top_services"])
        if not top_services.empty:
            st.bar_chart(top_services.set_index("service"), width="stretch")
        else:
            st.info("Ainda não há dados suficientes para o gráfico.")
        st.markdown("</div>", unsafe_allow_html=True)

    with table_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Status dos agendamentos")
        if not appointments.empty and "status" in appointments.columns:
            status_df = appointments["status"].value_counts().reset_index()
            status_df.columns = ["status", "quantidade"]
            st.dataframe(status_df, width="stretch", hide_index=True)
        else:
            st.info("Sem status para exibir.")
        st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Ver dados brutos de agendamentos"):
        if not appointments.empty:
            st.dataframe(appointments, width="stretch", hide_index=True)

elif page == "Agenda":
    hero()
    section_title("Agenda inteligente", "Crie e visualize agendamentos conectados aos clientes, serviços e profissionais.")

    clients = api_get("/clients")
    services = api_get("/services")
    professionals = api_get("/professionals")
    appointments = api_get("/appointments")

    client_map = {f"{item['name']} · ID {item['id']}": item for item in clients}
    service_map = {f"{item['name']} · {format_currency(item['price'])}": item for item in services}
    professional_map = {f"{item['name']} · {item['specialty']}": item for item in professionals}

    with st.container(border=True):
        st.markdown("### Novo agendamento")
        if not clients or not services or not professionals:
            st.warning("Cadastre pelo menos um cliente, um serviço e um profissional antes de criar agendamentos.")
        else:
            with st.form("appointment_form"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    selected_client = st.selectbox("Cliente", list(client_map.keys()))
                    scheduled_date = st.date_input("Data", value=datetime.now().date() + timedelta(days=1))
                with c2:
                    selected_service = st.selectbox("Serviço", list(service_map.keys()))
                    scheduled_time = st.time_input("Horário", value=time(14, 0))
                with c3:
                    selected_professional = st.selectbox("Profissional", list(professional_map.keys()))
                    custom_price = st.number_input("Preço final", min_value=0.0, value=float(service_map[selected_service]["price"]))

                submitted = st.form_submit_button("Salvar agendamento")
                if submitted:
                    scheduled_at = datetime.combine(scheduled_date, scheduled_time).isoformat()
                    api_post(
                        "/appointments",
                        json={
                            "client_id": client_map[selected_client]["id"],
                            "service_id": service_map[selected_service]["id"],
                            "professional_id": professional_map[selected_professional]["id"],
                            "scheduled_at": scheduled_at,
                            "final_price": float(custom_price),
                        },
                    )
                    st.success("Agendamento criado com sucesso. Atualize a página para ver na lista.")

    appt_df = pd.DataFrame(appointments)
    if not appt_df.empty:
        clients_by_id = {item["id"]: item["name"] for item in clients}
        services_by_id = {item["id"]: item["name"] for item in services}
        professionals_by_id = {item["id"]: item["name"] for item in professionals}
        appt_df["cliente"] = appt_df["client_id"].map(clients_by_id)
        appt_df["serviço"] = appt_df["service_id"].map(services_by_id)
        appt_df["profissional"] = appt_df["professional_id"].map(professionals_by_id)
        appt_df["valor"] = appt_df["final_price"].apply(format_currency)
        visible_cols = ["scheduled_at", "cliente", "serviço", "profissional", "status", "valor"]
        st.markdown("### Próximos e últimos agendamentos")
        st.dataframe(appt_df[visible_cols], width="stretch", hide_index=True)
    else:
        st.info("Nenhum agendamento encontrado.")

elif page == "Assistente IA":
    hero()
    section_title("Assistente IA para gestão e atendimento", "Use IA para criar respostas, ideias comerciais e mensagens mais profissionais.")

    col1, col2 = st.columns([1.05, 0.95])
    with col1:
        with st.container(border=True):
            st.markdown("### Mentora de gestão")
            business_context = st.text_input(
                "Contexto do negócio",
                "salão de beleza com serviços de cabelo, estética facial, unhas e bem-estar",
            )
            question = st.text_area(
                "Pergunta para a IA",
                "Como posso reduzir faltas nos agendamentos e aumentar o retorno das clientes?",
                height=140,
            )
            if st.button("Perguntar para a IA"):
                with st.spinner("Gerando resposta..."):
                    result = api_post("/ai/chat", json={"question": question, "business_context": business_context})
                    st.markdown(result["answer"])

    with col2:
        with st.container(border=True):
            st.markdown("### Mensagem para WhatsApp")
            goal = st.text_input("Objetivo", "confirmar agendamento de hidratação amanhã às 14h")
            client_profile = st.text_input("Perfil da cliente", "cliente recorrente que gosta de atendimento acolhedor")
            tone = st.text_input("Tom", "profissional, simpático e objetivo")
            if st.button("Criar mensagem"):
                with st.spinner("Criando mensagem..."):
                    result = api_post("/ai/message", json={"goal": goal, "client_profile": client_profile, "tone": tone})
                    st.success(result["message"])

elif page == "Recomendador":
    hero()
    section_title("Recomendador inteligente", "Sugira serviços de acordo com perfil, interesses, orçamento e objetivo da cliente.")

    with st.container(border=True):
        profile = st.text_area(
            "Perfil da cliente",
            "Cliente com cabelo cacheado e ressecado, busca brilho, redução de frizz e quer gastar até R$ 160.",
            height=150,
        )
        top_k = st.slider("Quantidade de recomendações", 1, 5, 3)

        if st.button("Recomendar serviços"):
            with st.spinner("Analisando perfil e serviços..."):
                result = api_post("/recommendations", json={"client_profile": profile, "top_k": top_k})
                recommendations = result["recommendations"]
                if recommendations:
                    for index, item in enumerate(recommendations, start=1):
                        with st.container(border=True):
                            c1, c2 = st.columns([0.72, 0.28])
                            with c1:
                                st.markdown(f"### {index}. {item['name']}")
                                st.write(item["description"])
                                st.caption(item["reason"])
                            with c2:
                                st.metric("Score", item["score"])
                                st.write(f"**Categoria:** {item['category']}")
                                st.write(f"**Preço:** {format_currency(item['price'])}")
                                st.write(f"**Duração:** {item['duration_minutes']} min")
                else:
                    st.warning("Nenhum serviço encontrado. Cadastre serviços primeiro.")

elif page == "Clientes":
    hero()
    section_title("Clientes", "Cadastre e consulte perfis para personalizar atendimento, vendas e recomendações.")

    with st.expander("Cadastrar cliente", expanded=True):
        with st.form("client_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                name = st.text_input("Nome")
                phone = st.text_input("Telefone")
            with c2:
                email = st.text_input("E-mail")
                hair_type = st.text_input("Tipo de cabelo")
            with c3:
                skin_type = st.text_input("Tipo de pele")
                interests = st.text_input("Interesses")
            notes = st.text_area("Observações")
            submitted = st.form_submit_button("Salvar cliente")
            if submitted:
                api_post(
                    "/clients",
                    json={
                        "name": name,
                        "phone": phone,
                        "email": email or None,
                        "hair_type": hair_type or None,
                        "skin_type": skin_type or None,
                        "interests": interests or None,
                        "notes": notes or None,
                    },
                )
                st.success("Cliente cadastrado com sucesso.")

    clients = safe_dataframe(api_get("/clients"), "Nenhum cliente cadastrado ainda.")
    if not clients.empty:
        st.dataframe(clients, width="stretch", hide_index=True)

elif page == "Serviços":
    hero()
    section_title("Serviços", "Monte um catálogo bonito e organizado para alimentar agenda, IA e recomendações.")

    with st.expander("Cadastrar serviço", expanded=True):
        with st.form("service_form"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Nome do serviço")
                category = st.text_input("Categoria")
                duration = st.number_input("Duração em minutos", min_value=10, value=60)
            with c2:
                price = st.number_input("Preço", min_value=0.0, value=100.0)
                tags = st.text_input("Tags", "cabelo hidratação beleza")
            description = st.text_area("Descrição")
            submitted = st.form_submit_button("Salvar serviço")
            if submitted:
                api_post(
                    "/services",
                    json={
                        "name": name,
                        "category": category,
                        "description": description,
                        "duration_minutes": int(duration),
                        "price": float(price),
                        "tags": tags,
                    },
                )
                st.success("Serviço cadastrado com sucesso.")

    services = safe_dataframe(api_get("/services"), "Nenhum serviço cadastrado ainda.")
    if not services.empty:
        services_display = services.copy()
        if "price" in services_display.columns:
            services_display["price"] = services_display["price"].apply(format_currency)
        st.dataframe(services_display, width="stretch", hide_index=True)

elif page == "Marketing IA":
    hero()
    section_title("Criador de marketing com IA", "Gere posts para Instagram, chamadas comerciais e campanhas rápidas para atrair agendamentos.")

    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            service_name = st.text_input("Serviço", "Hidratação Profunda")
        with c2:
            target_audience = st.text_input("Público-alvo", "mulheres com cabelo ressecado que buscam brilho e maciez")
        with c3:
            campaign_goal = st.text_input("Objetivo", "atrair agendamentos para a semana")

        if st.button("Gerar post"):
            with st.spinner("Criando conteúdo..."):
                result = api_post(
                    "/ai/marketing-post",
                    params={
                        "service_name": service_name,
                        "target_audience": target_audience,
                        "campaign_goal": campaign_goal,
                    },
                )
                st.markdown("### Conteúdo gerado")
                st.markdown(result["post"])

    st.markdown(
        """
        <div class="footer-note">
            Dica: depois você pode evoluir esta tela para gerar calendário editorial, legendas, hashtags e imagens com IA.
        </div>
        """,
        unsafe_allow_html=True,
    )

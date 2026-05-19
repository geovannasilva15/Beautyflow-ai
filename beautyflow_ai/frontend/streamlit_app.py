from __future__ import annotations

from datetime import datetime, time, timedelta

import pandas as pd
import streamlit as st

from api_client import api_get, api_online, api_post, format_currency
from auth import init_auth_state, logout_user, render_login_page
from styles import apply_global_styles


st.set_page_config(
    page_title="BeautyFlow AI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_styles()


def safe_dataframe(data: list[dict] | pd.DataFrame, empty_message: str) -> pd.DataFrame:
    df = pd.DataFrame(data)

    if df.empty:
        st.info(empty_message)

    return df


def page_header(title: str, subtitle: str) -> None:
    st.markdown(f"# {title}")
    st.caption(subtitle)
    st.write("")


init_auth_state()

if not st.session_state.authenticated:
    render_login_page()
    st.stop()


PAGE_MAP = {
    "🏠 Início": "home",
    "📊 Dashboard": "dashboard",
    "📅 Agenda": "agenda",
    "🤖 Assistente IA": "assistant",
    "🧠 Recomendador": "recommender",
    "👥 Clientes": "clients",
    "💇 Serviços": "services",
    "📣 Marketing IA": "marketing",
}


with st.sidebar:
    current_user = st.session_state.user

    st.markdown("## 💎 BeautyFlow AI")
    st.caption("Gestão inteligente para beleza e estética.")

    st.write("---")
    st.markdown(f"**Usuária:** {current_user['name']}")
    st.caption(current_user["role"])

    if st.button("Sair da conta"):
        logout_user()

    st.write("---")

    selected_label = st.radio("Menu", list(PAGE_MAP.keys()), label_visibility="collapsed")
    page = PAGE_MAP[selected_label]

    st.write("---")

    if api_online():
        st.success("API conectada")
    else:
        st.error("API offline")

    st.caption("API docs: http://127.0.0.1:8000/docs")


if not api_online():
    st.error("API não encontrada. Abra outro terminal e rode:")
    st.code("python -m uvicorn app.main:app --reload", language="powershell")
    st.stop()


if page == "home":
    page_header(
        "BeautyFlow AI",
        "Sistema inteligente para gestão de beleza, estética, agenda, clientes, IA e marketing.",
    )

    dashboard = api_get("/dashboard")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Clientes", dashboard["total_clients"])

    with c2:
        st.metric("Agendamentos", dashboard["total_appointments"])

    with c3:
        st.metric("Receita estimada", format_currency(dashboard["estimated_revenue"]))

    with c4:
        st.metric("Ticket médio", format_currency(dashboard["average_ticket"]))

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("### 📊 Gestão visual")
            st.write("Dashboard com receita, clientes, agenda, ticket médio e no-show.")
            st.caption("Dashboard · Métricas · Gestão")

    with col2:
        with st.container(border=True):
            st.markdown("### 🤖 Assistente IA")
            st.write("Geração de respostas, mensagens, ideias comerciais e atendimento.")
            st.caption("LLM · IA generativa · Automação")

    with col3:
        with st.container(border=True):
            st.markdown("### 🧠 Recomendador")
            st.write("Sugestão de serviços com base no perfil e objetivo da cliente.")
            st.caption("Machine Learning · Python · Recomendação")

    st.write("")

    with st.container(border=True):
        st.markdown("### Próximas evoluções")
        st.write("✅ Login real com banco de dados")
        st.write("✅ Agendamento público")
        st.write("✅ Integração com WhatsApp")
        st.write("✅ Deploy online")
        st.write("✅ Geração de imagens com IA")


elif page == "dashboard":
    page_header(
        "Dashboard executivo",
        "Acompanhe os principais indicadores do negócio.",
    )

    data = api_get("/dashboard")
    appointments = safe_dataframe(api_get("/appointments"), "Ainda não existem agendamentos cadastrados.")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Clientes", data["total_clients"])

    with c2:
        st.metric("Agendamentos", data["total_appointments"])

    with c3:
        st.metric("Receita estimada", format_currency(data["estimated_revenue"]))

    with c4:
        st.metric("Ticket médio", format_currency(data["average_ticket"]))

    st.write("")

    c5, c6, c7 = st.columns(3)

    with c5:
        st.metric("Concluídos", data["completed_appointments"])

    with c6:
        st.metric("Marcados", data["scheduled_appointments"])

    with c7:
        st.metric("Taxa de no-show", f"{data['no_show_rate'] * 100:.1f}%")

    st.write("")

    left, right = st.columns([1.25, 1])

    with left:
        with st.container(border=True):
            st.markdown("### Serviços mais agendados")
            top_services = pd.DataFrame(data["top_services"])

            if not top_services.empty:
                st.bar_chart(top_services.set_index("service"))
            else:
                st.info("Ainda não há dados suficientes para o gráfico.")

    with right:
        with st.container(border=True):
            st.markdown("### Status dos agendamentos")

            if not appointments.empty and "status" in appointments.columns:
                status_df = appointments["status"].value_counts().reset_index()
                status_df.columns = ["status", "quantidade"]
                st.dataframe(status_df, width="stretch", hide_index=True)
            else:
                st.info("Sem status para exibir.")

    with st.expander("Ver dados brutos"):
        if not appointments.empty:
            st.dataframe(appointments, width="stretch", hide_index=True)


elif page == "agenda":
    page_header(
        "Agenda inteligente",
        "Crie e visualize agendamentos conectados aos clientes, serviços e profissionais.",
    )

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
            with st.form("appointment_form_unique"):
                a1, a2, a3 = st.columns(3)

                with a1:
                    selected_client = st.selectbox("Cliente", list(client_map.keys()))
                    scheduled_date = st.date_input("Data", value=datetime.now().date() + timedelta(days=1))

                with a2:
                    selected_service = st.selectbox("Serviço", list(service_map.keys()))
                    scheduled_time = st.time_input("Horário", value=time(14, 0))

                with a3:
                    selected_professional = st.selectbox("Profissional", list(professional_map.keys()))
                    custom_price = st.number_input(
                        "Preço final",
                        min_value=0.0,
                        value=float(service_map[selected_service]["price"]),
                    )

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

                    st.success("Agendamento criado com sucesso.")
                    st.rerun()

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

        st.markdown("### Agendamentos")
        st.dataframe(appt_df[visible_cols], width="stretch", hide_index=True)
    else:
        st.info("Nenhum agendamento encontrado.")


elif page == "assistant":
    page_header(
        "Assistente IA",
        "Use IA para criar respostas, ideias comerciais e mensagens profissionais.",
    )

    c1, c2 = st.columns([1.05, 0.95])

    with c1:
        with st.container(border=True):
            st.markdown("### Mentora de gestão")

            business_context = st.text_input(
                "Contexto do negócio",
                "salão de beleza com serviços de cabelo, estética facial, unhas e bem-estar",
            )

            question = st.text_area(
                "Pergunta para a IA",
                "Como posso reduzir faltas nos agendamentos e aumentar o retorno das clientes?",
                height=150,
            )

            if st.button("Perguntar para a IA"):
                with st.spinner("Gerando resposta..."):
                    result = api_post(
                        "/ai/chat",
                        json={
                            "question": question,
                            "business_context": business_context,
                        },
                    )

                    st.markdown(result["answer"])

    with c2:
        with st.container(border=True):
            st.markdown("### Mensagem para WhatsApp")

            goal = st.text_input("Objetivo", "confirmar agendamento de hidratação amanhã às 14h")
            client_profile = st.text_input("Perfil da cliente", "cliente recorrente que gosta de atendimento acolhedor")
            tone = st.text_input("Tom", "profissional, simpático e objetivo")

            if st.button("Criar mensagem"):
                with st.spinner("Criando mensagem..."):
                    result = api_post(
                        "/ai/message",
                        json={
                            "goal": goal,
                            "client_profile": client_profile,
                            "tone": tone,
                        },
                    )

                    st.success(result["message"])


elif page == "recommender":
    page_header(
        "Recomendador inteligente",
        "Sugira serviços de acordo com perfil, interesses, orçamento e objetivo da cliente.",
    )

    with st.container(border=True):
        profile = st.text_area(
            "Perfil da cliente",
            "Cliente com cabelo cacheado e ressecado, busca brilho, redução de frizz e quer gastar até R$ 160.",
            height=150,
        )

        top_k = st.slider("Quantidade de recomendações", 1, 5, 3)

        if st.button("Recomendar serviços"):
            with st.spinner("Analisando perfil e serviços..."):
                result = api_post(
                    "/recommendations",
                    json={
                        "client_profile": profile,
                        "top_k": top_k,
                    },
                )

                recommendations = result["recommendations"]

                if recommendations:
                    for index, item in enumerate(recommendations, start=1):
                        with st.container(border=True):
                            r1, r2 = st.columns([0.72, 0.28])

                            with r1:
                                st.markdown(f"### {index}. {item['name']}")
                                st.write(item["description"])
                                st.caption(item["reason"])

                            with r2:
                                st.metric("Score", item["score"])
                                st.write(f"**Categoria:** {item['category']}")
                                st.write(f"**Preço:** {format_currency(item['price'])}")
                                st.write(f"**Duração:** {item['duration_minutes']} min")
                else:
                    st.warning("Nenhum serviço encontrado. Cadastre serviços primeiro.")


elif page == "clients":
    page_header(
        "Clientes",
        "Cadastre e consulte perfis para personalizar atendimento, vendas e recomendações.",
    )

    with st.expander("Cadastrar cliente", expanded=True):
        with st.form("client_form_unique"):
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
                st.rerun()

    clients = safe_dataframe(api_get("/clients"), "Nenhum cliente cadastrado ainda.")

    if not clients.empty:
        st.dataframe(clients, width="stretch", hide_index=True)


elif page == "services":
    page_header(
        "Serviços",
        "Monte um catálogo para alimentar agenda, IA e recomendações.",
    )

    with st.expander("Cadastrar serviço", expanded=True):
        with st.form("service_form_unique"):
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
                st.rerun()

    services = safe_dataframe(api_get("/services"), "Nenhum serviço cadastrado ainda.")

    if not services.empty:
        services_display = services.copy()

        if "price" in services_display.columns:
            services_display["price"] = services_display["price"].apply(format_currency)

        st.dataframe(services_display, width="stretch", hide_index=True)


elif page == "marketing":
    page_header(
        "Marketing IA",
        "Gere posts para Instagram, campanhas rápidas e chamadas comerciais.",
    )

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

    with st.container(border=True):
        st.markdown("### Evolução sugerida")
        st.write("Calendário editorial, hashtags automáticas, criador de campanhas e geração de imagem com IA.")
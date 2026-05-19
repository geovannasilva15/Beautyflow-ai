from __future__ import annotations

import streamlit as st

from styles import apply_login_styles


DEMO_USERS = {
    "geovanna@beautyflow.ai": {
        "password": "123456",
        "name": "Geovanna Silva",
        "role": "Fundadora",
    },
    "admin@beautyflow.ai": {
        "password": "123456",
        "name": "Admin BeautyFlow",
        "role": "Administrador",
    },
}


def init_auth_state() -> None:
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "user" not in st.session_state:
        st.session_state.user = None


def login_user(email: str, password: str) -> bool:
    email = email.strip().lower()
    user = DEMO_USERS.get(email)

    if user and user["password"] == password:
        st.session_state.authenticated = True
        st.session_state.user = {
            "email": email,
            "name": user["name"],
            "role": user["role"],
        }
        return True

    return False


def logout_user() -> None:
    st.session_state.authenticated = False
    st.session_state.user = None
    st.rerun()


def render_login_page() -> None:
    apply_login_styles()

    st.markdown(
        """
        <div style="text-align:center; margin-bottom: 24px;">
            <div style="
                width: 60px;
                height: 60px;
                border-radius: 20px;
                background: linear-gradient(135deg, #ec4899, #8b5cf6);
                display: inline-flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 30px;
                box-shadow: 0 14px 35px rgba(236,72,153,0.28);
            ">💎</div>

            <h1 style="
                margin: 14px 0 6px 0;
                font-size: 2.4rem;
                letter-spacing: -0.06em;
                color: #1f1630;
            ">BeautyFlow AI</h1>

            <p style="
                margin: 0;
                color: #6d607e;
                font-size: 0.98rem;
                line-height: 1.6;
            ">
                Plataforma inteligente para gestão de beleza, estética e bem-estar.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown("## Entrar no painel")
        st.caption("Acesse sua central de gestão, agenda, clientes e IA.")
        st.write("")

        with st.form("login_form_unique"):
            email = st.text_input("E-mail", value="geovanna@beautyflow.ai")
            password = st.text_input("Senha", value="123456", type="password")

            submitted = st.form_submit_button("Entrar")

            if submitted:
                if login_user(email, password):
                    st.success("Login realizado com sucesso.")
                    st.rerun()
                else:
                    st.error("E-mail ou senha incorretos.")

        st.info(
            """
            **Acesso demo**

            E-mail: geovanna@beautyflow.ai  
            Senha: 123456
            """
        )

    st.caption("Projeto MVP para portfólio · Python · IA · Machine Learning")
from app.core.config import get_settings
from app.services.rag_service import SimpleRAG

settings = get_settings()
rag = SimpleRAG()


def generate_ai_answer(question: str, business_context: str) -> str:
    snippets = rag.retrieve(question, top_k=3)
    context = "\n\n".join(snippets) if snippets else "Sem contexto local encontrado."

    prompt = f"""
Você é a Bella, uma mentora virtual para negócios de beleza, estética e bem-estar.
Responda em português do Brasil, com linguagem clara, prática e profissional.
Use o contexto local quando ele fizer sentido.

Contexto do negócio: {business_context}

Base de conhecimento:
{context}

Pergunta da pessoa usuária:
{question}

Entregue uma resposta objetiva, com passos acionáveis e sugestões realistas para pequenos negócios.
""".strip()

    if settings.openai_api_key:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=settings.openai_api_key)
            response = client.responses.create(
                model=settings.openai_model,
                input=prompt,
            )
            return response.output_text
        except Exception as exc:
            return _fallback_answer(question, context, error=str(exc))

    return _fallback_answer(question, context)


def generate_client_message(goal: str, client_profile: str, tone: str) -> str:
    prompt = f"""
Crie uma mensagem curta para WhatsApp para um negócio de beleza.
Objetivo: {goal}
Perfil do cliente: {client_profile}
Tom: {tone}
Regras: seja humano, profissional, sem exageros, com chamada para ação.
""".strip()

    if settings.openai_api_key:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=settings.openai_api_key)
            response = client.responses.create(
                model=settings.openai_model,
                input=prompt,
            )
            return response.output_text
        except Exception:
            pass

    return (
        "Olá! Tudo bem? Passando para te lembrar que temos horários disponíveis e "
        "podemos te ajudar com um atendimento pensado para o seu momento. "
        "Me chama por aqui para escolhermos o melhor serviço e horário para você."
    )


def generate_marketing_post(service_name: str, target_audience: str, campaign_goal: str) -> str:
    prompt = f"""
Crie um post para Instagram de um negócio de beleza.
Serviço: {service_name}
Público: {target_audience}
Objetivo da campanha: {campaign_goal}
Inclua: legenda, CTA e 5 hashtags.
""".strip()

    if settings.openai_api_key:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=settings.openai_api_key)
            response = client.responses.create(
                model=settings.openai_model,
                input=prompt,
            )
            return response.output_text
        except Exception:
            pass

    return (
        f"Seu momento de cuidado começa aqui. O serviço de {service_name} foi pensado para quem busca "
        f"mais autoestima, praticidade e bem-estar. Agende seu horário e viva essa experiência.\n\n"
        "CTA: Chame no WhatsApp e garanta seu horário.\n"
        "#beleza #autocuidado #salaodebeleza #estetica #bemestar"
    )


def _fallback_answer(question: str, context: str, error: str | None = None) -> str:
    base = (
        "Ainda estou no modo sem LLM real, mas já consigo sugerir um caminho prático.\n\n"
        "1. Entenda o objetivo do cliente: atendimento, venda, retorno, fidelização ou redução de faltas.\n"
        "2. Use dados simples: serviços mais vendidos, horários vazios, clientes inativos e ticket médio.\n"
        "3. Crie uma ação direta: mensagem personalizada, oferta de pacote, lembrete ou campanha.\n"
        "4. Meça o resultado: respostas, agendamentos, comparecimento e faturamento.\n\n"
        f"Pergunta recebida: {question}\n\n"
        f"Contexto recuperado da base local:\n{context}"
    )
    if error:
        base += f"\n\nAviso técnico: a chamada ao provedor de IA falhou e usei o fallback local. Erro: {error}"
    return base

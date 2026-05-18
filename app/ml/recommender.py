from sqlmodel import Session, select
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.db.models import Service


def recommend_services(session: Session, client_profile: str, top_k: int = 3) -> list[dict]:
    services = session.exec(select(Service).where(Service.active == True)).all()  # noqa: E712
    if not services:
        return []

    service_texts = [
        f"{s.name} {s.category} {s.description} {s.tags}".lower()
        for s in services
    ]

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(service_texts + [client_profile.lower()])
    profile_vector = matrix[-1]
    service_matrix = matrix[:-1]
    scores = cosine_similarity(profile_vector, service_matrix).flatten()

    ranked_indexes = scores.argsort()[::-1][:top_k]
    recommendations = []

    for idx in ranked_indexes:
        service = services[idx]
        recommendations.append(
            {
                "service_id": service.id,
                "name": service.name,
                "category": service.category,
                "description": service.description,
                "price": service.price,
                "duration_minutes": service.duration_minutes,
                "score": round(float(scores[idx]), 4),
                "reason": _build_reason(service, client_profile),
            }
        )

    return recommendations


def _build_reason(service: Service, client_profile: str) -> str:
    profile = client_profile.lower()
    tags = service.tags.lower()
    matches = []

    for word in ["cabelo", "hidratação", "pele", "manicure", "sobrancelha", "limpeza", "cronograma", "progressiva", "massagem", "estética"]:
        if word in profile and word in tags:
            matches.append(word)

    if matches:
        return f"Combina com o perfil informado por ter relação com: {', '.join(matches)}."
    return "Serviço recomendado pela similaridade entre o perfil do cliente e a descrição do catálogo."

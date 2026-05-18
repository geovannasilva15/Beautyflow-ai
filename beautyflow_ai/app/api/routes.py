from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db.database import get_session
from app.db.models import Appointment, Client, Professional, Service
from app.ml.recommender import recommend_services
from app.schemas.schemas import (
    AIChatRequest,
    AIMessageRequest,
    AppointmentCreate,
    AppointmentUpdateStatus,
    ClientCreate,
    RecommendationRequest,
    ServiceCreate,
)
from app.services.ai_service import generate_ai_answer, generate_client_message, generate_marketing_post
from app.services.analytics_service import get_dashboard_metrics

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok", "message": "BeautyFlow AI API está funcionando."}


@router.post("/clients", response_model=Client)
def create_client(payload: ClientCreate, session: Session = Depends(get_session)) -> Client:
    client = Client(**payload.model_dump())
    session.add(client)
    session.commit()
    session.refresh(client)
    return client


@router.get("/clients", response_model=list[Client])
def list_clients(session: Session = Depends(get_session)) -> list[Client]:
    return session.exec(select(Client).order_by(Client.created_at.desc())).all()


@router.post("/services", response_model=Service)
def create_service(payload: ServiceCreate, session: Session = Depends(get_session)) -> Service:
    service = Service(**payload.model_dump())
    session.add(service)
    session.commit()
    session.refresh(service)
    return service


@router.get("/services", response_model=list[Service])
def list_services(session: Session = Depends(get_session)) -> list[Service]:
    return session.exec(select(Service).where(Service.active == True)).all()  # noqa: E712


@router.get("/professionals", response_model=list[Professional])
def list_professionals(session: Session = Depends(get_session)) -> list[Professional]:
    return session.exec(select(Professional).where(Professional.active == True)).all()  # noqa: E712


@router.post("/appointments", response_model=Appointment)
def create_appointment(payload: AppointmentCreate, session: Session = Depends(get_session)) -> Appointment:
    client = session.get(Client, payload.client_id)
    service = session.get(Service, payload.service_id)
    professional = session.get(Professional, payload.professional_id)

    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado.")
    if not professional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado.")

    appointment = Appointment(
        client_id=payload.client_id,
        service_id=payload.service_id,
        professional_id=payload.professional_id,
        scheduled_at=payload.scheduled_at,
        final_price=payload.final_price if payload.final_price is not None else service.price,
    )
    session.add(appointment)
    session.commit()
    session.refresh(appointment)
    return appointment


@router.get("/appointments", response_model=list[Appointment])
def list_appointments(session: Session = Depends(get_session)) -> list[Appointment]:
    return session.exec(select(Appointment).order_by(Appointment.scheduled_at.desc())).all()


@router.patch("/appointments/{appointment_id}/status", response_model=Appointment)
def update_appointment_status(
    appointment_id: int,
    payload: AppointmentUpdateStatus,
    session: Session = Depends(get_session),
) -> Appointment:
    appointment = session.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")
    appointment.status = payload.status
    session.add(appointment)
    session.commit()
    session.refresh(appointment)
    return appointment


@router.post("/ai/chat")
def ai_chat(payload: AIChatRequest) -> dict:
    answer = generate_ai_answer(payload.question, payload.business_context)
    return {"answer": answer}


@router.post("/ai/message")
def ai_message(payload: AIMessageRequest) -> dict:
    message = generate_client_message(payload.goal, payload.client_profile, payload.tone)
    return {"message": message}


@router.post("/ai/marketing-post")
def ai_marketing_post(service_name: str, target_audience: str, campaign_goal: str) -> dict:
    post = generate_marketing_post(service_name, target_audience, campaign_goal)
    return {"post": post}


@router.post("/recommendations")
def recommendations(payload: RecommendationRequest, session: Session = Depends(get_session)) -> dict:
    items = recommend_services(session, payload.client_profile, payload.top_k)
    return {"recommendations": items}


@router.get("/dashboard")
def dashboard(session: Session = Depends(get_session)) -> dict:
    return get_dashboard_metrics(session)

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.db.models import AppointmentStatus


class ClientCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    hair_type: Optional[str] = None
    skin_type: Optional[str] = None
    interests: Optional[str] = None
    notes: Optional[str] = None


class ServiceCreate(BaseModel):
    name: str
    category: str
    description: str
    duration_minutes: int
    price: float
    tags: str = ""


class AppointmentCreate(BaseModel):
    client_id: int
    service_id: int
    professional_id: int
    scheduled_at: datetime
    final_price: Optional[float] = None


class AppointmentUpdateStatus(BaseModel):
    status: AppointmentStatus


class AIChatRequest(BaseModel):
    question: str = Field(..., min_length=3)
    business_context: str = "salão de beleza, estética e bem-estar"


class AIMessageRequest(BaseModel):
    goal: str = Field(..., description="Objetivo da mensagem. Ex: confirmar horário, recuperar cliente, vender pacote.")
    client_profile: str = "cliente de salão de beleza"
    tone: str = "profissional, acolhedor e persuasivo"


class RecommendationRequest(BaseModel):
    client_profile: str = Field(..., description="Descreva cabelo, pele, interesses, histórico, orçamento e objetivo do cliente.")
    top_k: int = 3

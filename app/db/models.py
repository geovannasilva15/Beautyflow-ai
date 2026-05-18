from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel


class AppointmentStatus(str, Enum):
    scheduled = "scheduled"
    completed = "completed"
    canceled = "canceled"
    no_show = "no_show"


class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone: str
    email: Optional[str] = None
    hair_type: Optional[str] = None
    skin_type: Optional[str] = None
    interests: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Professional(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    specialty: str
    active: bool = True


class Service(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category: str
    description: str
    duration_minutes: int
    price: float
    tags: str = ""
    active: bool = True


class Appointment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id")
    service_id: int = Field(foreign_key="service.id")
    professional_id: int = Field(foreign_key="professional.id")
    scheduled_at: datetime
    status: AppointmentStatus = AppointmentStatus.scheduled
    final_price: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

from datetime import datetime, timedelta
from app.db.models import Appointment, AppointmentStatus, Client, Professional, Service


def get_seed_clients() -> list[Client]:
    return [
        Client(
            name="Mariana Costa",
            phone="(11) 99999-0001",
            email="mariana@email.com",
            hair_type="cabelo cacheado e ressecado",
            skin_type="pele mista",
            interests="hidratação, cronograma capilar, sobrancelha",
            notes="Prefere atendimento aos sábados.",
        ),
        Client(
            name="Camila Rocha",
            phone="(11) 99999-0002",
            email="camila@email.com",
            hair_type="cabelo liso com química",
            skin_type="pele oleosa",
            interests="progressiva, reconstrução, limpeza de pele",
            notes="Cliente recorrente, costuma comprar pacotes.",
        ),
        Client(
            name="Fernanda Lima",
            phone="(11) 99999-0003",
            email="fernanda@email.com",
            hair_type="cabelo ondulado",
            skin_type="pele sensível",
            interests="manicure, pedicure, spa dos pés, design de sobrancelhas",
            notes="Gosta de promoções em dias úteis.",
        ),
    ]


def get_seed_professionals() -> list[Professional]:
    return [
        Professional(name="Aline Santos", specialty="Cabelos e tratamentos capilares"),
        Professional(name="Bruna Ferreira", specialty="Estética facial"),
        Professional(name="Larissa Alves", specialty="Manicure, pedicure e sobrancelhas"),
    ]


def get_seed_services() -> list[Service]:
    return [
        Service(
            name="Hidratação Profunda",
            category="Cabelos",
            description="Tratamento para devolver brilho, maciez e água aos fios ressecados.",
            duration_minutes=60,
            price=120.0,
            tags="cabelo hidratação ressecado brilho cronograma capilar cacheado ondulado",
        ),
        Service(
            name="Reconstrução Capilar",
            category="Cabelos",
            description="Tratamento indicado para fios danificados por química, calor ou quebra.",
            duration_minutes=75,
            price=160.0,
            tags="cabelo reconstrução química quebra progressiva danificado tratamento capilar",
        ),
        Service(
            name="Progressiva Premium",
            category="Cabelos",
            description="Alinhamento dos fios com acabamento liso, redução de volume e efeito disciplinado.",
            duration_minutes=180,
            price=350.0,
            tags="cabelo progressiva liso volume química alinhamento fios",
        ),
        Service(
            name="Limpeza de Pele Inteligente",
            category="Estética Facial",
            description="Higienização, esfoliação e cuidado facial para pele oleosa, mista ou com cravos.",
            duration_minutes=90,
            price=180.0,
            tags="pele limpeza estética facial oleosa mista cravos skincare",
        ),
        Service(
            name="Design de Sobrancelhas",
            category="Beleza Facial",
            description="Mapeamento facial e design para valorizar o olhar de forma natural.",
            duration_minutes=40,
            price=65.0,
            tags="sobrancelha design olhar facial beleza natural",
        ),
        Service(
            name="Manicure e Pedicure",
            category="Unhas",
            description="Cuidado completo para mãos e pés, com esmaltação tradicional.",
            duration_minutes=90,
            price=75.0,
            tags="manicure pedicure unhas esmaltação mãos pés beleza",
        ),
        Service(
            name="Spa dos Pés",
            category="Bem-estar",
            description="Relaxamento, hidratação e cuidado para pés cansados e ressecados.",
            duration_minutes=60,
            price=95.0,
            tags="spa pés relaxamento hidratação bem-estar ressecado",
        ),
        Service(
            name="Massagem Relaxante",
            category="Bem-estar",
            description="Massagem para relaxamento, alívio de tensão e experiência de autocuidado.",
            duration_minutes=60,
            price=140.0,
            tags="massagem relaxante bem-estar autocuidado tensão relaxamento",
        ),
    ]


def get_seed_appointments() -> list[Appointment]:
    now = datetime.utcnow()
    return [
        Appointment(client_id=1, service_id=1, professional_id=1, scheduled_at=now - timedelta(days=10), status=AppointmentStatus.completed, final_price=120.0),
        Appointment(client_id=2, service_id=3, professional_id=1, scheduled_at=now - timedelta(days=8), status=AppointmentStatus.completed, final_price=350.0),
        Appointment(client_id=3, service_id=6, professional_id=3, scheduled_at=now - timedelta(days=5), status=AppointmentStatus.completed, final_price=75.0),
        Appointment(client_id=1, service_id=5, professional_id=3, scheduled_at=now - timedelta(days=2), status=AppointmentStatus.no_show, final_price=65.0),
        Appointment(client_id=2, service_id=4, professional_id=2, scheduled_at=now + timedelta(days=2), status=AppointmentStatus.scheduled, final_price=180.0),
        Appointment(client_id=3, service_id=7, professional_id=3, scheduled_at=now + timedelta(days=4), status=AppointmentStatus.scheduled, final_price=95.0),
    ]

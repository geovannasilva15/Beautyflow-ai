from sqlmodel import Session, select
from app.db.models import Appointment, AppointmentStatus, Client, Service


def get_dashboard_metrics(session: Session) -> dict:
    clients = session.exec(select(Client)).all()
    services = session.exec(select(Service)).all()
    appointments = session.exec(select(Appointment)).all()

    completed = [a for a in appointments if a.status == AppointmentStatus.completed]
    scheduled = [a for a in appointments if a.status == AppointmentStatus.scheduled]
    no_show = [a for a in appointments if a.status == AppointmentStatus.no_show]

    revenue = sum(a.final_price for a in completed)
    avg_ticket = revenue / len(completed) if completed else 0
    no_show_rate = len(no_show) / len(appointments) if appointments else 0

    service_lookup = {s.id: s.name for s in services}
    service_counts: dict[str, int] = {}
    for appointment in appointments:
        service_name = service_lookup.get(appointment.service_id, "Serviço removido")
        service_counts[service_name] = service_counts.get(service_name, 0) + 1

    top_services = sorted(
        [{"service": name, "appointments": count} for name, count in service_counts.items()],
        key=lambda item: item["appointments"],
        reverse=True,
    )

    return {
        "total_clients": len(clients),
        "total_services": len(services),
        "total_appointments": len(appointments),
        "scheduled_appointments": len(scheduled),
        "completed_appointments": len(completed),
        "no_show_appointments": len(no_show),
        "estimated_revenue": round(revenue, 2),
        "average_ticket": round(avg_ticket, 2),
        "no_show_rate": round(no_show_rate, 4),
        "top_services": top_services[:10],
    }

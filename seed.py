from sqlmodel import Session, select
from app.db.database import create_db_and_tables, engine
from app.db.models import Appointment, Client, Professional, Service
from data.sample_data import get_seed_appointments, get_seed_clients, get_seed_professionals, get_seed_services


def seed() -> None:
    create_db_and_tables()
    with Session(engine) as session:
        has_clients = session.exec(select(Client)).first()
        if has_clients:
            print("Banco já possui dados. Seed não foi executado novamente.")
            return

        clients = get_seed_clients()
        professionals = get_seed_professionals()
        services = get_seed_services()

        for item in clients + professionals + services:
            session.add(item)
        session.commit()

        appointments = get_seed_appointments()
        for appointment in appointments:
            session.add(appointment)
        session.commit()

        print("Seed executado com sucesso. Dados iniciais criados.")


if __name__ == "__main__":
    seed()

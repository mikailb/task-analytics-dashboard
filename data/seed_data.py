from models.task import db, Task
import random
from datetime import datetime, timedelta
import os

# Konstanter for å generere tilfeldig data
CATEGORIES = ['Utvikling', 'Testing', 'Design', 'Dokumentasjon', 'Møter', 'Feilretting']
PRIORITIES = ['Høy', 'Medium', 'Lav']
STATUSES = ['Ikke påbegynt', 'Pågående', 'Fullført']
USERS = ['Per Hansen', 'Lise Olsen', 'Erik Nilsen', 'Anna Pedersen', 'Ola Nordmann']

def random_date(start_date, end_date):
    """Generer en tilfeldig dato mellom start_date og end_date"""
    delta = end_date - start_date
    random_days = random.randrange(delta.days)
    return start_date + timedelta(days=random_days)

def seed_database():
    """Fyller databasen med tilfeldig genererte oppgaver"""
    # Opprett datoområde - siste 6 måneder
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    # Opprett 100 tilfeldige oppgaver
    tasks = []
    for i in range(1, 101):
        # Generer tilfeldige datoer
        created_at = random_date(start_date, end_date)
        due_date = created_at + timedelta(days=random.randint(1, 30))
        
        # Bestem status og sett completed_at hvis fullført
        status = random.choice(STATUSES)
        completed_at = None
        if status == 'Fullført':
            completed_at = min(due_date + timedelta(days=random.randint(-5, 5)), datetime.now())
        
        # Estimer og sett faktiske timer
        estimated_hours = round(random.uniform(1, 40), 1)
        actual_hours = None
        if status == 'Fullført':
            # Faktiske timer varierer rundt estimert tid
            variance = random.uniform(0.7, 1.3)
            actual_hours = round(estimated_hours * variance, 1)
        
        # Opprett ny oppgave
        task = Task(
            title=f'Oppgave {i}',
            description=f'Dette er beskrivelsen for oppgave {i}. Generert som testdata.',
            category=random.choice(CATEGORIES),
            priority=random.choice(PRIORITIES),
            status=status,
            created_at=created_at,
            updated_at=created_at + timedelta(days=random.randint(0, 10)),
            due_date=due_date,
            completed_at=completed_at,
            assigned_to=random.choice(USERS),
            estimated_hours=estimated_hours,
            actual_hours=actual_hours
        )
        db.session.add(task)
    
    # Commit endringer til databasen
    db.session.commit()
    print("Database seeded with 100 random tasks.")

if __name__ == "__main__":
    # Dette kjøres kun hvis skriptet kjøres direkte
    from app import app
    with app.app_context():
        seed_database()
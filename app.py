from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
import json

app = Flask(__name__)

# Oppsett av absolutt sti til databasen
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'data', 'sample_tasks.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'din-hemmelige-nøkkel-her'
app.config['DEBUG'] = True

# Sørg for at data-mappen eksisterer
data_dir = os.path.join(basedir, 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Kontekstprosessor for å gjøre nåværende dato tilgjengelig i alle maler
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Importerer databasen og modeller etter at app er konfigurert
from models.task import db, Task
from services.analytics import (
    get_task_completion_stats,
    get_task_category_distribution,
    get_avg_completion_time,
    get_productivity_trend
)

# Initialiserer databasen
db.init_app(app)

@app.route('/')
def index():
    """Hovedside med dashboardoversikt"""
    return render_template('index.html')

@app.route('/tasks')
def tasks():
    """Side for oppgaveoversikt"""
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/analytics')
def analytics():
    """Detaljert analyseside"""
    return render_template('analytics.html')

@app.route('/api/task-completion')
def task_completion_data():
    """API-endepunkt for oppgavegjennomføringsdata"""
    data = get_task_completion_stats()
    return jsonify(data)

@app.route('/api/category-distribution')
def category_distribution_data():
    """API-endepunkt for kategorifordelingsdata"""
    data = get_task_category_distribution()
    return jsonify(data)

@app.route('/api/avg-completion-time')
def avg_completion_time_data():
    """API-endepunkt for gjennomsnittlig fullføringstidsdata"""
    data = get_avg_completion_time()
    return jsonify(data)

@app.route('/api/productivity-trend')
def productivity_trend_data():
    """API-endepunkt for produktivitetstrenddata"""
    data = get_productivity_trend()
    return jsonify(data)

@app.route('/api/tasks')
def tasks_data():
    """API-endepunkt for råoppgavedata"""
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

if __name__ == '__main__':
    # Opprett databasen hvis den ikke finnes
    with app.app_context():
        try:
            db.create_all()
            print(f"Database created at {database_path}")
            
            # Sjekk om databasen er tom
            if Task.query.count() == 0:
                # Importer og kjør seeddata-skript
                from data.seed_data import seed_database
                seed_database()
                print("Database seeded with sample data")
        except Exception as e:
            print(f"Database error: {e}")
    
    app.run(debug=True)
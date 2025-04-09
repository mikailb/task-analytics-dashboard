from flask import Flask, render_template, request, jsonify
from models.task import db, Task
from services.analytics import (
    get_task_completion_stats,
    get_task_category_distribution,
    get_avg_completion_time,
    get_productivity_trend
)
import os
import json

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# Initialisere databasen
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
        if not os.path.exists('data/sample_tasks.db'):
            db.create_all()
            # Importer og kjør seeddata-skript hvis databasen er tom
            from data.seed_data import seed_database
            seed_database()
    
    app.run(debug=True)
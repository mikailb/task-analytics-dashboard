from models.task import Task, db
import pandas as pd
from sqlalchemy import func, extract
from datetime import datetime, timedelta

def get_task_completion_stats():
    """
    Henter oppgavegjennomføringsstatistikk per måned.
    Returnerer data i formatet egnet for en linjegraf.
    """
    # Hent data fra databasen
    tasks = Task.query.all()
    
    # Konverter til pandas dataframe
    df = pd.DataFrame([{
        'created_at': task.created_at,
        'completed_at': task.completed_at,
        'status': task.status
    } for task in tasks])
    
    # Filter ut oppgaver uten created_at
    if df.empty or 'created_at' not in df.columns:
        return {'labels': [], 'created': [], 'completed': []}
    
    df = df[df['created_at'].notna()]
    
    # Legg til månedskategori for aggregering
    df['year_month'] = df['created_at'].dt.strftime('%Y-%m')
    
    # Opprett dataframe for fullførte oppgaver
    completed_df = df[df['status'] == 'Fullført'].copy()
    if not completed_df.empty and 'completed_at' in completed_df.columns:
        completed_df['completion_year_month'] = completed_df['completed_at'].dt.strftime('%Y-%m')
    
    # Aggreger data per måned
    created_by_month = df.groupby('year_month').size()
    
    completed_by_month = pd.Series(0, index=created_by_month.index)
    if not completed_df.empty and 'completion_year_month' in completed_df.columns:
        temp_completed = completed_df.groupby('completion_year_month').size()
        for month in temp_completed.index:
            if month in completed_by_month.index:
                completed_by_month[month] = temp_completed[month]
    
    # Sorter etter måned
    months = sorted(created_by_month.index)
    
    return {
        'labels': months,
        'created': created_by_month[months].tolist(),
        'completed': completed_by_month[months].tolist()
    }

def get_task_category_distribution():
    """
    Henter fordelingen av oppgaver etter kategori.
    Returnerer data i formatet egnet for et kakediagram.
    """
    # Utfør en SQL-spørring for å telle oppgaver per kategori
    result = db.session.query(
        Task.category, 
        func.count(Task.id).label('count')
    ).group_by(Task.category).all()
    
    categories = [r[0] for r in result]
    counts = [r[1] for r in result]
    
    return {
        'labels': categories,
        'data': counts
    }

def get_avg_completion_time():
    """
    Beregner gjennomsnittlig fullføringstid (i dager) per kategori.
    Returnerer data i formatet egnet for et stolpediagram.
    """
    # Hent fullførte oppgaver
    tasks = Task.query.filter(
        Task.status == 'Fullført',
        Task.completed_at.isnot(None),
        Task.created_at.isnot(None)
    ).all()
    
    # Beregn fullføringstid per oppgave og gruppert etter kategori
    category_completion_times = {}
    
    for task in tasks:
        completion_time = (task.completed_at - task.created_at).days
        if task.category not in category_completion_times:
            category_completion_times[task.category] = []
        category_completion_times[task.category].append(completion_time)
    
    # Beregn gjennomsnitt per kategori
    categories = []
    avg_times = []
    
    for category, times in category_completion_times.items():
        categories.append(category)
        avg_times.append(sum(times) / len(times))
    
    return {
        'labels': categories,
        'data': avg_times
    }

def get_productivity_trend():
    """
    Beregner produktivitetstrender basert på antall fullførte oppgaver og faktisk tid brukt.
    Returnerer data i formatet egnet for en kombinert graf.
    """
    # Hent fullførte oppgaver med faktisk tid
    tasks = Task.query.filter(
        Task.status == 'Fullført',
        Task.completed_at.isnot(None),
        Task.actual_hours.isnot(None)
    ).all()
    
    # Konverter til pandas dataframe
    df = pd.DataFrame([{
        'completed_at': task.completed_at,
        'actual_hours': task.actual_hours
    } for task in tasks])
    
    if df.empty:
        return {'labels': [], 'tasks_count': [], 'avg_hours': []}
    
    # Legg til månedskategori for aggregering
    df['year_month'] = df['completed_at'].dt.strftime('%Y-%m')
    
    # Aggreger data per måned
    monthly_data = df.groupby('year_month').agg(
        tasks_count=('actual_hours', 'count'),
        total_hours=('actual_hours', 'sum')
    )
    
    monthly_data['avg_hours'] = monthly_data['total_hours'] / monthly_data['tasks_count']
    
    # Sorter etter måned
    months = sorted(monthly_data.index)
    
    return {
        'labels': months,
        'tasks_count': monthly_data.loc[months, 'tasks_count'].tolist(),
        'avg_hours': monthly_data.loc[months, 'avg_hours'].tolist()
    }
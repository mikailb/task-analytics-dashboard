from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(20), nullable=False)  # High, Medium, Low
    status = db.Column(db.String(20), nullable=False)  # Not Started, In Progress, Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    assigned_to = db.Column(db.String(100), nullable=True)
    estimated_hours = db.Column(db.Float, nullable=True)
    actual_hours = db.Column(db.Float, nullable=True)
    
    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'
    
    def to_dict(self):
        """Konverter oppgaveobjekt til dictionary for JSON-serialisering"""
        task_dict = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'priority': self.priority,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'assigned_to': self.assigned_to,
            'estimated_hours': self.estimated_hours,
            'actual_hours': self.actual_hours
        }
        return task_dict
from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(50), default='student')  # 'student', 'admin', etc.
    
    def __repr__(self):
        return f'<User {self.username}>'

class Institution(db.Model):
    __tablename__ = 'institutions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    website = db.Column(db.String(255))
    
    applications = db.relationship('Application', backref='institution', lazy=True)
    
    def __repr__(self):
        return f'<Institution {self.name}>'

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'), nullable=False)
    program = db.Column(db.String(255), nullable=False)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending')  # 'pending', 'accepted', 'rejected'
    
    def __repr__(self):
        return f'<Application {self.program} for {self.institution.name} by {self.user.username}>'

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(10))
    nationality = db.Column(db.String(50))
    address = db.Column(db.String(255))
    
    user = db.relationship('User', backref='student_details', lazy=True)
    
    def __repr__(self):
        return f'<Student {self.user.username}>'

class ApplicationStatus(db.Model):
    __tablename__ = 'application_status'
    
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    status_update = db.Column(db.String(255), nullable=False)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    application = db.relationship('Application', backref='status_updates', lazy=True)
    
    def __repr__(self):
        return f'<Status Update for Application {self.application.id} - {self.status_update}>'

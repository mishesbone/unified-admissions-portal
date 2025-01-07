#backend/routes/students.py
#
from flask import Blueprint, jsonify, request
from app.models import User, Application
from app import db

# Create a Blueprint for student-related routes
students_bp = Blueprint('students', __name__)

# Route for getting a list of all applications
@students_bp.route('/applications', methods=['GET'])
def get_applications():
    applications = Application.query.all()

    # Serialize the results
    applications_data = [{
        'id': application.id,
        'user_id': application.user_id,
        'institution_id': application.institution_id,
        'program': application.program
    } for application in applications]

    return jsonify(applications_data), 200

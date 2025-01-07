
#backend/routes/search.py
#
from flask import Blueprint, request, jsonify
from app.models import Institution, Application, User
from app import db

# Create a Blueprint for search routes
search_bp = Blueprint('search', __name__)

# Route for searching institutions by name or location
@search_bp.route('/institutions', methods=['GET'])
def search_institutions():
    query = request.args.get('query', '')
    institutions = Institution.query.filter(
        (Institution.name.ilike(f'%{query}%')) | 
        (Institution.location.ilike(f'%{query}%'))
    ).all()

    # Serialize the results
    institutions_data = [{
        'id': institution.id,
        'name': institution.name,
        'location': institution.location,
        'description': institution.description
    } for institution in institutions]

    return jsonify(institutions_data), 200

# Route for searching applications by user ID
@search_bp.route('/applications', methods=['GET'])
def search_applications():
    user_id = request.args.get('user_id', '')
    applications = Application.query.filter_by(user_id=user_id).all()

    # Serialize the results
    applications_data = [{
        'id': application.id,
        'user_id': application.user_id,
        'institution_id': application.institution_id,
        'program': application.program
    } for application in applications]

    return jsonify(applications_data), 200

# Route for searching users by username or email
@search_bp.route('/users', methods=['GET'])
def search_users():
    query = request.args.get('query', '')
    users = User.query.filter(
        (User.username.ilike(f'%{query}%')) | 
        (User.email.ilike(f'%{query}%'))
    ).all()

    # Serialize the results
    users_data = [{
        'id': user.id,
        'username': user.username,
        'email': user.email
    } for user in users]

    return jsonify(users_data), 200

# Route for searching all data by a given query
@search_bp.route('/all', methods=['GET'])
def search_all():
    query = request.args.get('query', '')
    institutions = Institution.query.filter(
        (Institution.name.ilike(f'%{query}%')) | 
        (Institution.location.ilike(f'%{query}%'))
    ).all()

    applications = Application.query.filter(
        (Application.program.ilike(f'%{query}%'))
    ).all()

    users = User.query.filter(
        (User.username.ilike(f'%{query}%')) | 
        (User.email.ilike(f'%{query}%'))
    ).all()

    # Serialize the results
    institutions_data = [{
        'id': institution.id,
        'name': institution.name,
        'location': institution.location,
        'description': institution.description
    } for institution in institutions]

    applications_data = [{
        'id': application.id,
        'user_id': application.user_id,
        'institution_id': application.institution_id,
        'program': application.program
    } for application in applications]

    users_data = [{
        'id': user.id,
        'username': user.username,
        'email': user.email
    } for user in users]

    return jsonify({
        'institutions': institutions_data,
        'applications': applications_data,
        'users': users_data
    }), 200

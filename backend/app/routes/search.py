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

# Route for searching programs offered by institutions
@search_bp.route('/programs', methods=['GET'])
def search_programs():
    query = request.args.get('query', '')
    applications = Application.query.filter(
        Application.program.ilike(f'%{query}%')
    ).all()

    # Serialize the results
    programs_data = [{
        'id': app.id,
        'program': app.program,
        'user_id': app.user_id,
        'institution_id': app.institution_id
    } for app in applications]

    return jsonify(programs_data), 200

# Route for searching users based on username or email
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

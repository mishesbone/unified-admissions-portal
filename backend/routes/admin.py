#backend/routes/admin.py
#
from flask import Blueprint, jsonify, request
from app.models import User, Application, Institution
from app import db

# Create a Blueprint for admin-related routes
admin_bp = Blueprint('admin', __name__)

# Route for getting a list of all users
@admin_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()

    # Serialize the results
    users_data = [{
        'id': user.id,
        'username': user.username,
        'email': user.email
    } for user in users]

    return jsonify(users_data), 200

# Route for getting a list of all applications
@admin_bp.route('/applications', methods=['GET'])
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

# Route for adding a new institution
@admin_bp.route('/institutions', methods=['POST'])
def add_institution():
    data = request.get_json()
    name = data.get('name')
    location = data.get('location')
    description = data.get('description')

    if not name or not location:
        return jsonify({"msg": "Name and location are required"}), 400

    new_institution = Institution(name=name, location=location, description=description)

    try:
        db.session.add(new_institution)
        db.session.commit()
        return jsonify({
            'id': new_institution.id,
            'name': new_institution.name,
            'location': new_institution.location,
            'description': new_institution.description
        }), 201
    except:
        return jsonify({"msg": "An error occurred while adding the institution"}), 500

# Route for deleting an institution by ID
@admin_bp.route('/institutions/<int:id>', methods=['DELETE'])
def delete_institution(id):
    institution = Institution.query.get(id)

    if not institution:
        return jsonify({"msg": "Institution not found"}), 404

    try:
        db.session.delete(institution)
        db.session.commit()
        return jsonify({"msg": "Institution deleted successfully"}), 200
    except:
        return jsonify({"msg": "An error occurred while deleting the institution"}), 500

# Route for updating an existing institution
@admin_bp.route('/institutions/<int:id>', methods=['PUT'])
def update_institution(id):
    institution = Institution.query.get(id)

    if not institution:
        return jsonify({"msg": "Institution not found"}), 404

    data = request.get_json()
    name = data.get('name')
    location = data.get('location')
    description = data.get('description')

    if not name or not location:
        return jsonify({"msg": "Name and location are required"}), 400

    institution.name = name
    institution.location = location
    institution.description = description

    try:
        db.session.commit()
        return jsonify({
            'id': institution.id,
            'name': institution.name,
            'location': institution.location,
            'description': institution.description
        }), 200
    except:
        return jsonify({"msg": "An error occurred while updating the institution"}), 500

# Route for deleting a user by ID
@admin_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "User deleted successfully"}), 200
    except:
        return jsonify({"msg": "An error occurred while deleting the user"}), 500

# Route for getting a list of all institutions
@admin_bp.route('/institutions', methods=['GET'])
def get_institutions():
    institutions = Institution.query.all()

    # Serialize the results
    institutions_data = [{
        'id': institution.id,
        'name': institution.name,
        'location': institution.location,
        'description': institution.description
    } for institution in institutions]

    return jsonify(institutions_data), 200

# Route for getting detailed information about a specific user
@admin_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    }), 200

# Route for getting detailed information about a specific institution
@admin_bp.route('/institutions/<int:id>', methods=['GET'])
def get_institution(id):
    institution = Institution.query.get(id)

    if not institution:
        return jsonify({"msg": "Institution not found"}), 404

    return jsonify({
        'id': institution.id,
        'name': institution.name,
        'location': institution.location,
        'description': institution.description
    }), 200

# Route for updating an existing user
@admin_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')

    if not username or not email:
        return jsonify({"msg": "Username and email are required"}), 400

    user.username = username
    user.email = email

    try:
        db.session.commit()
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email
        }), 200
    except:
        return jsonify({"msg": "An error occurred while updating the user"}), 500

# Route for getting detailed information about a specific application
@admin_bp.route('/applications/<int:id>', methods=['GET'])
def get_application(id):
    application = Application.query.get(id)

    if not application:
        return jsonify({"msg": "Application not found"}), 404

    return jsonify({
        'id': application.id,
        'user_id': application.user_id,
        'institution_id': application.institution_id,
        'program': application.program
    }), 200

# Route for updating an existing application
@admin_bp.route('/applications/<int:id>', methods=['PUT'])
def update_application(id):
    application = Application.query.get(id)

    if not application:
        return jsonify({"msg": "Application not found"}), 404

    data = request.get_json()
    user_id = data.get('user_id')
    institution_id = data.get('institution_id')
    program = data.get('program')

    if not user_id or not institution_id or not program:
        return jsonify({"msg": "User ID, institution ID, and program are required"}), 400

    application.user_id = user_id
    application.institution_id = institution_id
    application.program = program

    try:
        db.session.commit()
        return jsonify({
            'id': application.id,
            'user_id': application.user_id,
            'institution_id': application.institution_id,
            'program': application.program
        }), 200
    except:
        return jsonify({"msg": "An error occurred while updating the application"}), 500

# Route for deleting an application by ID
@admin_bp.route('/applications/<int:id>', methods=['DELETE'])
def delete_application(id):
    application = Application.query.get(id)

    if not application:
        return jsonify({"msg": "Application not found"}), 404

    try:
        db.session.delete(application)
        db.session.commit()
        return jsonify({"msg": "Application deleted successfully"}), 200
    except:
        return jsonify({"msg": "An error occurred while deleting the application"}), 500

# Route for searching all data by a given query
@admin_bp.route('/search', methods=['GET'])
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

# Route for searching users by username or email
@admin_bp.route('/search/users', methods=['GET'])
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

    return jsonify(users_data),
#         'id': user.id,
#         'username': user.username,
#         'email': user.email
#     } for user in users]

#     return jsonify(users_data), 200
#
#     return jsonify(users_data), 200

# Route for searching applications by user ID
@admin_bp.route('/search/applications', methods=['GET'])
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

# Route for searching institutions by name or location
@admin_bp.route('/search/institutions', methods=['GET'])
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
    return jsonify(institutions_data), 200

# Route for searching applications by program
@admin_bp.route('/search/applications', methods=['GET'])
def search_applications():
    query = request.args.get('query', '')
    applications = Application.query.filter(
        (Application.program.ilike(f'%{query}%'))
    ).all()

    # Serialize the results
    applications_data = [{
        'id': application.id,
        'user_id': application.user_id,
        'institution_id': application.institution_id,
        'program': application.program
    } for application in applications]

    return jsonify(applications_data), 200
    return jsonify(applications_data), 200

# Route for searching applications by college
@admin_bp.route('/search/applications', methods=['GET'])
def search_applications():
    query = request.args.get('query', '')
    applications = Application.query.filter(
        (Application.program.ilike(f'%{query}%'))
    ).all()

    # Serialize the results
    applications_data = [{
        'id': application.id,
        'user_id': application.user_id,
        'institution_id': application.institution_id,
        'program': application.program
    } for application in applications]

    return jsonify(applications_data), 200
    return jsonify(applications_data), 200
    return jsonify(applications_data), 200


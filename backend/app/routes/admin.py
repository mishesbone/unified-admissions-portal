from flask import Blueprint, request, jsonify
from app.models import User, Institution, Application
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

# Route for getting detailed information about a specific user
@admin_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Return the user's details
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    }), 200

# Route for deleting a user
@admin_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Delete the user from the database
    db.session.delete(user)
    db.session.commit()

    return jsonify({'msg': 'User deleted successfully'}), 200

# Route for viewing all institutions
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

# Route for viewing all applications
@admin_bp.route('/applications', methods=['GET'])
def get_applications():
    applications = Application.query.all()

    # Serialize the results
    applications_data = [{
        'id': app.id,
        'user_id': app.user_id,
        'institution_id': app.institution_id,
        'program': app.program
    } for app in applications]

    return jsonify(applications_data), 200

# Route for viewing system statistics (e.g., number of users, institutions, applications)
@admin_bp.route('/stats', methods=['GET'])
def get_stats():
    # Count the number of users, institutions, and applications
    user_count = User.query.count()
    institution_count = Institution.query.count()
    application_count = Application.query.count()

    stats = {
        'users': user_count,
        'institutions': institution_count,
        'applications': application_count
    }

    return jsonify(stats), 200

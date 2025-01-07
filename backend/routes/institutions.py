#backend/routes/institutions.py
#
from flask import Blueprint, jsonify, request
from app.models import Institution, Application
from app import db

# Create a Blueprint for institution-related routes
institutions_bp = Blueprint('institutions', __name__)

# Route for getting a list of all institutions
@institutions_bp.route('/institutions', methods=['GET'])
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

# Route for getting detailed information about a specific institution
@institutions_bp.route('/institutions/<int:id>', methods=['GET'])
def get_institution(id):
    institution = Institution.query.get(id)

    if not institution:
        return jsonify({"msg": "Institution not found"}), 404

    # Return the institution's details
    return jsonify({
        'id': institution.id,
        'name': institution.name,
        'location': institution.location,
        'description': institution.description
    }), 200

# Route for adding a new institution
@institutions_bp.route('/institutions', methods=['POST'])
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
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "An error occurred while adding the institution"}), 500

# Route for updating an existing institution
@institutions_bp.route('/institutions/<int:id>', methods=['PUT'])
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
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "An error occurred while updating the institution
"}), 500

# Route for deleting an institution
@institutions_bp.route('/institutions/<int:id>', methods=['DELETE'])
def delete_institution(id):
    institution = Institution.query.get(id)

    if not institution:
        return jsonify({"msg": "Institution not found"}), 404

    try:
        db.session.delete(institution)
        db.session.commit()
        return jsonify({'msg': 'Institution deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "An error occurred while deleting the institution"}), 500

        
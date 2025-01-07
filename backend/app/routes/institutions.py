from flask import Blueprint, request, jsonify
from app.models import Institution
from app import db

# Create a Blueprint for institutions-related routes
institutions_bp = Blueprint('institutions', __name__)

# Route for creating a new institution
@institutions_bp.route('/', methods=['POST'])
def create_institution():
    data = request.get_json()

    # Extract fields from the request
    name = data.get('name')
    location = data.get('location')
    description = data.get('description')

    if not name or not location:
        return jsonify({"msg": "Missing required fields: name, location"}), 400

    # Create a new Institution object
    new_institution = Institution(
        name=name,
        location=location,
        description=description
    )

    # Add the new institution to the database
    db.session.add(new_institution)
    db.session.commit()

    return jsonify({
        'msg': 'Institution created successfully',
        'institution': {
            'id': new_institution.id,
            'name': new_institution.name,
            'location': new_institution.location,
            'description': new_institution.description
        }
    }), 201

# Route for getting all institutions
@institutions_bp.route('/', methods=['GET'])
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

# Route for getting an institution by ID
@institutions_bp.route('/<int:id>', methods=['GET'])
def get_institution(id):
    institution = Institution.query.get(id)

    if not institution:
        return jsonify({"msg": "Institution not found"}), 404

    # Return the institution details
    return jsonify({
        'id': institution.id,
        'name': institution.name,
        'location': institution.location,
        'description': institution.description
    }), 200

# Route for updating an institution by ID
@institutions_bp.route('/<int:id>', methods=['PUT'])
def update_institution(id):
    data = request.get_json()
    institution = Institution.query.get(id)

    if not institution:
        return jsonify({"msg": "Institution not found"}), 404

    # Update the institution's details
    institution.name = data.get('name', institution.name)
    institution.location = data.get('location', institution.location)
    institution.description = data.get('description', institution.description)

    # Commit the changes to the database
    db.session.commit()

    return jsonify({
        'msg': 'Institution updated successfully',
        'institution': {
            'id': institution.id,
            'name': institution.name,
            'location': institution.location,
            'description': institution.description
        }
    }), 200

# Route for deleting an institution by ID
@institutions_bp.route('/<int:id>', methods=['DELETE'])
def delete_institution(id):
    institution = Institution.query.get(id)

    if not institution:
        return jsonify({"msg": "Institution not found"}), 404

    # Delete the institution from the database
    db.session.delete(institution)
    db.session.commit()

    return jsonify({'msg': 'Institution deleted successfully'}), 200

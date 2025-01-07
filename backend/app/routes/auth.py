from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

# Route for user registration
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Extract the fields from the request
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    # Check if the user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "Email already registered"}), 400

    # Hash the password and create a new user
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_password)

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201

# Route for user login (generates JWT token)
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Extract the fields from the request
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    # Check if the user exists and verify the password
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"msg": "Invalid email or password"}), 401

    # Create JWT token for the user
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

# Route for checking if the user is logged in (protected route)
@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({
        'msg': f'Hello, {user.username}',
        'user_id': user.id
    }), 200

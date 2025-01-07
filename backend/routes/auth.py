#backend/routes/auth.py
#
from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from app.auth import generate_token, requires_auth, verify_token, verify_refresh_token, create_user, login_user, logout_user, refresh_token, revoke_token, get_user_id_from_token, get_user_id_from_refresh_token

# Create a Blueprint for auth-related routes
auth_bp = Blueprint('auth', __name__)

# Route for registering a new user
@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"msg": "Username, email, and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already exists"}), 400

    user = create_user(username, email, password)

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user
    }), 201

# Route for logging in a user
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Email and password are required"}), 400

    user = login_user(email, password)

    if not user:
        return jsonify({"msg": "Invalid credentials"}), 401

    token = generate_token(user.id)
    refresh_token = generate_token(user.id, is_refresh=True)

    return jsonify({
        'token': token,
        'refresh_token': refresh_token
    }), 200

# Route for logging out a user
@auth_bp.route('/logout', methods=['POST'])
@requires_auth
def logout():
    token = request.headers.get('Authorization').split()[1]
    user_id = get_user_id_from_token(token)

    logout_user(user_id)

    return jsonify({'msg': 'Logged out successfully'}), 200

# Route for refreshing a token
@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    refresh_token = data.get('refresh_token')

    if not refresh_token:
        return jsonify({"msg": "Refresh token is required"}), 400

    user_id = get_user_id_from_refresh_token(refresh_token)

    if not user_id:
        return jsonify({"msg": "Invalid refresh token"}), 401

    token = refresh_token(user_id)
    new_refresh_token = generate_token(user_id, is_refresh=True)

    return jsonify({
        'token': token,
        'refresh_token': new_refresh_token
    }), 200

# Route for revoking a token
@auth_bp.route('/revoke', methods=['POST'])
@requires_auth
def revoke():
    token = request.headers.get('Authorization').split()[1]
    user_id = get_user_id_from_token(token)

    revoke_token(token)

    return jsonify({'msg': 'Token revoked successfully'}), 200

# Route for getting the current user
@auth_bp.route('/user', methods=['GET'])
@requires_auth
def get_user():
    token = request.headers.get('Authorization').split()[1]
    user_id = get_user_id_from_token(token)

    user = User.query.get(user_id)

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    }), 200

# Route for updating the current user
@auth_bp.route('/user', methods=['PUT'])
@requires_auth
def update_user():
    token = request.headers.get('Authorization').split()[1]
    user_id = get_user_id_from_token(token)

    user = User.query.get(user_id)

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')

    if username:
        user.username = username

    if email:
        user.email = email

    db.session.commit()

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    }), 200

# Route for updating the current user's password
@auth_bp.route('/user/password', methods=['PUT'])
@requires_auth
def update_password():
    token = request.headers.get('Authorization').split()[1]
    user_id = get_user_id_from_token(token)

    user = User.query.get(user_id)

    data = request.get_json()
    password = data.get('password')

    if not password:
        return jsonify({"msg": "Password is required"}), 400

    user.set_password(password)
    db.session.commit()

    return jsonify({'msg': 'Password updated successfully'}), 200

# Route for deleting the current user
@auth_bp.route('/user', methods=['DELETE'])
@requires_auth
def delete_user():
    token = request.headers.get('Authorization').split()[1]
    user_id = get_user_id_from_token(token)

    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return jsonify({'msg': 'User deleted successfully'}), 200

# Route for getting all users
@auth_bp.route('/users', methods=['GET'])
@requires_auth
def get_users():
    users = User.query.all()

    users_data = [{
        'id': user.id,
        'username': user.username,
        'email': user.email
    } for user in users]

    return jsonify(users_data), 200

# Route for getting detailed information about a specific user
@auth_bp.route('/users/<int:id>', methods=['GET'])
@requires_auth
def get_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    }), 200



# Route for deleting a user
@auth_bp.route('/users/<int:id>', methods=['DELETE'])
@requires_auth
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'msg': 'User deleted successfully'}), 200

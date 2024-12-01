from flask import Blueprint, request, jsonify
from models import User
from database import db

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    """
    Login endpoint for user authentication.
    Validates username and password from the `users` table.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Check if user exists in the database
    user = User.query.filter_by(username=username).first()
    if not user or user.password != password:
        return jsonify({"error": "Invalid username or password"}), 401

    # If authentication succeeds, return user details and role
    return jsonify({
        "message": "Login successful",
        "user_id": user.id,
        "username": user.username,
        "role": user.role
    }), 200

@auth_blueprint.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieve user details by user ID.
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "role": user.role
    }), 200

@auth_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """
    Retrieve all users in the database.
    """
    users = User.query.all()
    result = [
        {
            "id": user.id,
            "username": user.username,
            "role": user.role
        } for user in users
    ]
    return jsonify(result), 200

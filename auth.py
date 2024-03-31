from flask import Blueprint, Flask, jsonify, request
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from flasgger import Swagger
from models import User
from mockdb import get_user_by_username, add_user

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user_record = get_user_by_username(username)
    #if a user is found, check_password_hash compares the provided password with the stored hashed password
    if user_record and check_password_hash(user_record['password'], password):
        user = User(username, user_record['id'])
        login_user(user)
        return jsonify({"status": "Logged in"})
    else:
        return jsonify({"status": "Login failed"}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    if add_user(username, password):
        return jsonify({"status": "Registration successful"}), 201
    else:
        return jsonify({"error": "User already exists"}), 409


@auth_bp.route('/logout')
def logout():
    logout_user()
    return jsonify({"status": "Logged out"})

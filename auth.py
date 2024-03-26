from flask import Blueprint, request, jsonify
from flask_login import login_user,logout_user
from werkzeug.security import check_password_hash
from models import User
from mockdb import get_user_by_username

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


@auth_bp.route('/logout')
def logout():
    logout_user()
    return jsonify({"status": "Logged out"})

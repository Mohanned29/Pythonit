
from flask import Flask, jsonify, request
from flask_login import LoginManager
from auth import auth_bp
from main import generate_schedule

app = Flask(__name__)

app.secret_key = 'abcdefghijklmnopqrstuvwxyz'

#chatgpt helped:
login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(auth_bp)

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.get(user_id)

@app.route('/api/schedule', methods=['GET'])
def get_schedule():

    return jsonify({"message": "Please specify a section for a detailed schedule."})

@app.route('/api/select_schedule', methods=['GET'])
def select_schedule():
    section_key = request.args.get('section_key')
    if section_key:
        schedule = generate_schedule(section_key)
        return jsonify(schedule)
    else:
        return jsonify({"error": "Section key not specified"}), 400

@app.route('/')
def home():
    return "Welcome to the Schedule Generator API!"

if __name__ == '__main__':
    app.run(debug=True)


# URL = http://localhost:5000/api/select_schedule?section_key=<SECTION_KEY>
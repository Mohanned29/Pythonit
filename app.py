from flask import Flask, jsonify
from main import generate_schedule

app = Flask(__name__)

@app.route('/api/schedule', methods=['GET'])
def get_schedule():
    schedule = generate_schedule()
    return jsonify(schedule)

@app.route('/')
def home():
    return "Welcome to the Schedule Generator API!"


if __name__ == '__main__':
    app.run(debug=True)

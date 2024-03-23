from flask import Flask, jsonify, request
from main import generate_schedule

app = Flask(__name__)

@app.route('/api/schedule', methods=['GET'])
def get_schedule():
    # This endpoint remains for backward compatibility or general use
    return jsonify({"message": "Please specify a section for a detailed schedule."})

@app.route('/api/select_schedule', methods=['GET'])
def select_schedule():
    section_key = request.args.get('section_key')  # Expecting format "2nd Year CS GTR - A"
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

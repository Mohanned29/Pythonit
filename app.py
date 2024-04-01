from flask import Flask, jsonify
from main import generate_schedules_for_all_sections, DataReader

app = Flask(__name__)

app.secret_key = 'abcdefghijklmnopqrstuvwxyz'


@app.route('/', methods=['GET'])
def get_all_schedules():
    try:
        rooms = DataReader.read_json_file('rooms.json')
        global_room_schedule = {}
        all_schedules = generate_schedules_for_all_sections(rooms, global_room_schedule)
        return jsonify(all_schedules), 200
    except Exception as e:
        error_type = type(e).__name__
        error_message = f"Error generating all schedules: {str(e) or 'Unknown Error'}, Type: {error_type}"
        print(error_message)
        return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)
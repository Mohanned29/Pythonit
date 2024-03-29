from data_reader import DataReader
from m_schedule_generator import ScheduleGenerator
import os

def file_exists(filename):
    # Check if a file exists in the current directory
    return os.path.isfile(filename)

def get_course_filename(section_key):
    # Determine the CSV file based on section_key
    filename_map = {
        "2INGA": "module2ING.csv",
        "2INGB": "module2ING.csv",
        "1INGA": "module1ING.csv",
        "1INGB": "module1ING.csv",
        "1INGC": "module1ING.csv",
        "1LMD1": "module1LMD.csv",
        "1LMD2": "module1LMD.csv",
        "1LMD3": "module1LMD.csv",
        "1LMD4": "module1LMD.csv",
        "1LMD5": "module1LMD.csv",
        "1LMD6": "module1LMD.csv",
        "2ISILA": "module2ISIL.csv",
        "2ISILB": "module2ISIL.csv",
        "2ACADA": "module2ACAD.csv",
        "2ACADB": "module2ACAD.csv",
        "2ACADC": "module2ACAD.csv",
        "2GTRA": "module2GTR.csv",
        "3ISILA": "module3ISIL.csv",
        "3ISILB": "module3ISIL.csv",
        "3ACADA": "module3ACAD.csv",
        "3ACADB": "module3ACAD.csv",
        "3GTRA": "module3GTR.csv"
    }
    return filename_map.get(section_key, None)

def generate_schedule(section_key):
    if not section_key:
        return {"error": "Section key not specified"}

    sections_data = DataReader.read_json_file('sections.json')
    rooms = DataReader.read_json_file('rooms.json')

    if section_key not in sections_data:
        return {"error": f"Section '{section_key}' not found in the sections data."}

    courses_filename = get_course_filename(section_key)
    if not courses_filename or not file_exists(courses_filename):
        return {"error": f"No course data found for the selected section: {section_key}"}

    courses = DataReader.read_courses_csv(courses_filename)

    days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
    times = ["8:00 - 09:30", "09:40 - 11:10", "11:20 - 12:50", "13:00 - 14:30", "14:40 - 16:10"]

    filtered_sections_data = {section_key: sections_data[section_key]}

    schedule_generator = ScheduleGenerator(rooms, days, times, courses, filtered_sections_data)
    section_schedule_filtered = schedule_generator.generate_schedule()

    # New implementation for formatted schedule
    formatted_schedule = {}
    year = section_key[0]
    department = section_key[1:-1]  # Extract the department abbreviation
    section = section_key[-1]

    formatted_schedule['description'] = f"{year}ème année {department} section {section}:"
    
    for day in days:
        formatted_schedule[day] = []

    for session in section_schedule_filtered:
        _, course_name, session_type, day, time, room = session
        formatted_schedule[day].append({
            "course_name": course_name,
            "session_type": session_type,
            "time": time,
            "room": room
        })
    
    return formatted_schedule

if __name__ == '__main__':
    print("This script should be used as an importable module.")

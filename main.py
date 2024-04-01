from data_reader import DataReader
from m_schedule_generator import ScheduleGenerator
import os


def file_exists(filename):
    return os.path.isfile(filename)


def get_course_filename(section_key):
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
        "1MATHA":"module1MATH.csv",
        "1MATHB":"module1MATH.csv",
        "1MATHC":"module1MATH.csv",
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
        "3GTRA": "module3GTR.csv",
        "4HPC":"module4HPC.csv",
        "4BIGDATA":"module4BIGDATA.csv",
        "4LI":"module4LI.csv",
        "4IV":"module4IV.csv",
        "4SII":"module4SII.csv",
        "4SSI":"module4SSI.csv"
    }
    return filename_map.get(section_key, None)


def generate_schedule(section_key, rooms, global_room_schedule):
    """Generate schedule for a given section key, considering global room schedule."""
    sections_data = DataReader.read_json_file('sections.json')
    course_filename = get_course_filename(section_key)
    if not course_filename or not file_exists(course_filename):
        return {"error": f"No course data found for the selected section: {section_key}"}
    
    courses = DataReader.read_courses_csv(course_filename)
    days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
    times = ["8:00 - 09:30", "09:40 - 11:10", "11:20 - 12:50", "13:00 - 14:30", "14:40 - 16:10"]

    schedule_generator = ScheduleGenerator(rooms, days, times, courses, {section_key: sections_data[section_key]})

    return schedule_generator.generate_schedule(global_room_schedule)


def generate_schedules_for_all_sections(rooms, global_room_schedule):
    sections_data = DataReader.read_json_file('sections.json')
    all_schedules = {}

    for section_key in sections_data.keys():
        schedule = generate_schedule(section_key, rooms, global_room_schedule)
        all_schedules[section_key] = schedule

    return all_schedules



if __name__ == '__main__':
    rooms = DataReader.read_json_file('rooms.json')
    global_room_schedule = {}  # Initialize global room schedule
    all_schedules = generate_schedules_for_all_sections(rooms, global_room_schedule)

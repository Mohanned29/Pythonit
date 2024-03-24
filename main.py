from data_reader import DataReader
from m_schedule_generator import ScheduleGenerator
import os

def file_exists(filename):
    """Check if a file exists in the current directory."""
    return os.path.isfile(filename)


def get_course_filename(program_year, section):
    """Determine the course CSV filename based on program year and specialization."""
    filename_map = {
        "1st Year Ingenieur CS": "module1ING.csv",
        "2nd Year Ingenieur CS": "module2ING.csv",
        "1st Year CS LMD": "module1LMD.csv",
        "2nd Year CS ISIL": "module2ISIL.csv",
        "2nd Year CS GTR": "module2GTR.csv",
        "2nd Year CS ACAD": "module2ACAD.csv"
    }

    key = program_year
    return filename_map.get(key)


def generate_schedule(section_key):
    days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
    times = ["8:00 - 09:30", "09:40 - 11:10", "11:20 - 12:50", "13:00 - 14:30", "14:40 - 16:10"]

    sections_data = DataReader.read_json_file('sections.json')
    rooms = DataReader.read_json_file('rooms.json')

    program_year, section = section_key.split(" - ")
    courses_filename = get_course_filename(program_year, section)
    if not courses_filename:
        return {"error": "No course data found for the selected section."}

    courses = DataReader.read_courses_csv(courses_filename)

    filtered_sections = {program_year: {section: sections_data[program_year][section]}}
    schedule_generator = ScheduleGenerator(rooms, days, times, courses, filtered_sections)
    schedule_generator.generate_schedule()

    return schedule_generator.schedule

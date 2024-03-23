from data_reader import DataReader
from m_schedule_generator import ScheduleGenerator
import os

def file_exists(filename):
    """Check if a file exists at the given path."""
    return os.path.isfile(filename)

def get_course_filename(program_year, section):
    """Determine the course CSV filename based on program year and section."""
    # Example: "module2ndYearCSGTR-A.csv"
    base_filename = f"module{program_year.replace(' ', '')}"
    section_specific_filename = f"{base_filename}{section}.csv"

    if file_exists(section_specific_filename):
        return section_specific_filename
    else:
        # Fallback to a general file if a specific one doesn't exist
        general_filename = f"{base_filename}.csv"
        return general_filename if file_exists(general_filename) else None

def generate_schedule(section_key):
    days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
    times = ["8:00 - 09:30", "09:40 - 11:10", "11:20 - 12:50", "13:00 - 14:30", "14:40 - 16:10"]

    sections_data = DataReader.read_json_file('sections.json')
    rooms = DataReader.read_json_file('rooms.json')

    # Split the section_key into program_year and section
    program_year, section = section_key.split(" - ")

    # Get the correct course filename based on the program year and section
    courses_filename = get_course_filename(program_year, section)
    if not courses_filename:
        return {"error": "No course data found for the selected section."}

    courses = DataReader.read_courses_csv(courses_filename)

    # Initialize ScheduleGenerator with the courses and sections relevant to the chosen section
    filtered_sections = {program_year: {section: sections_data[program_year][section]}}
    schedule_generator = ScheduleGenerator(rooms, days, times, courses, filtered_sections)
    schedule_generator.generate_schedule()

    return schedule_generator.schedule

from data_reader import DataReader
from m_schedule_generator import ScheduleGenerator

def generate_schedule():
    days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
    times = ["8:00 - 09:30", "09:40 - 11:10", "11:20 - 12:50", "13:00 - 14:30", "14:40 - 16:10"]

    sections = DataReader.read_json_file('sections.json')
    rooms = DataReader.read_json_file('rooms.json')
    courses = DataReader.read_courses_csv('module.csv')

    schedule_generator = ScheduleGenerator(rooms, days, times, courses, sections)
    schedule_generator.generate_schedule()

    generated_schedule = []
    for entry in schedule_generator.schedule:
        day, time, course_name, session_type, section_group, room = entry
        generated_schedule.append({
            "day": day,
            "time": time,
            "course_name": course_name,
            "session_type": session_type,
            "section_group": section_group,
            "room": room
        })

    return generated_schedule

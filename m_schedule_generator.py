import random

class ScheduleGenerator:
    def __init__(self, rooms, days, times, courses, sections):
        self.rooms = rooms
        self.days = days
        self.times = times
        self.courses = courses
        self.sections = sections
        self.schedule = []
        self.course_schedule_status = {
            course: {"lectures": False, "TD": False, "TP": False}
            for course in courses
        }
        self.initialize_availability()

    def initialize_availability(self):
        self.room_availability = {}
        for room_type, room_info_list in self.rooms.items():
            self.room_availability[room_type] = {}
            for room_info in room_info_list:
                room_name = room_info['name']
                self.room_availability[room_type][room_name] = {
                    'availability': set(
                        tuple(avail) for avail in room_info['availability']
                    ),
                    'sessions': [],
                }

        self.section_availability = {}
        for section, details in self.sections.items():
            self.section_availability[section] = set((d, t) for d in self.days for t in self.times)

    def is_section_available(self, section, day, time):
        return (day, time) in self.section_availability[section]


    def find_available_room(self, room_type, day, time):
        if room_type not in self.room_availability:
            return None
        available_rooms = [
            room_name for room_name, room_info in self.room_availability[room_type].items()
            if (day, time) in room_info['availability'] and len(room_info['sessions']) < len(self.sections)
        ]
        if available_rooms:
            return random.choice(available_rooms)
        return None

    def schedule_session(self, course_name, session_type, section, day, time, room):
        if self.check_course_schedule_status(course_name, session_type):
            return False
        self.schedule.append((section, course_name, session_type, day, time, room))
        self.room_availability[self.courses[course_name][session_type]][room]['sessions'].append((day, time))
        self.section_availability[section].remove((day, time))
        self.update_course_schedule_status(course_name, session_type)
        return True

    def generate_schedule(self):
        for section, details in self.sections.items():
            for course_name, sessions in self.courses.items():
                for session_type, room_type in sessions.items():
                    if not self.course_schedule_status[course_name][session_type]:
                        best_option = self.find_best_room_and_time(course_name, session_type, section)
                        if best_option:
                            day, time, room = best_option
                            self.schedule_session(course_name, session_type, section, day, time, room)
        return self.schedule

    #find the best available room and time for a session
    def find_best_room_and_time(self, course_name, session_type, section):
        best_option = None
        best_score = float('inf')

        for day in self.days:
            for time in self.times:
                if self.is_section_available(section, day, time):
                    room = self.find_available_room(self.courses[course_name][session_type], day, time)
                    if room:
                        score = self.days.index(day) * 100 + self.times.index(time)
                        if score < best_score:
                            best_score = score
                            best_option = (day, time, room)
        return best_option

    #check if a session is already scheduled
    def check_course_schedule_status(self, course_name, session_type):
        return self.course_schedule_status[course_name][session_type]

    #update the scheduled status of a session
    def update_course_schedule_status(self, course_name, session_type):
        self.course_schedule_status[course_name][session_type] = True

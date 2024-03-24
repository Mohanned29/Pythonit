class ScheduleGenerator:
    def __init__(self, rooms, days, times, courses, sections):
        self.rooms = rooms
        self.days = days
        self.times = times
        self.courses = courses
        self.sections = sections
        self.schedule = []
        # Tracks if a lecture, TD, or TP session has been scheduled for each course
        self.course_schedule_status = {
            course: {"lectures": False, "TD": False, "TP": False}
            for course in courses
        }
        self.initialize_availability()

    def initialize_availability(self):

        self.room_availability = {
            rtype: {room['name']: set(tuple(avail) for avail in room['availability'])
                    for room in rinfo}
            for rtype, rinfo in self.rooms.items()
        }
        self.section_availability = {
            py: {s: set((d, t) for d in self.days for t in self.times)
                    for s in sects}
            for py, sects in self.sections.items()
        }

    def check_course_schedule_status(self, program_year, section, course_name, session_type):
        return self.course_schedule_status[course_name][session_type]

    def update_course_schedule_status(self, program_year, section, course_name, session_type):
        self.course_schedule_status[course_name][session_type] = True

    def is_section_available(self, program_year, section, day, time):
        return (day, time) in self.section_availability[program_year][section]

    def find_available_room(self, room_type, day, time):
        print(f"Looking for {room_type} on {day} at {time}")
        if room_type not in self.room_availability:
            print(f"Room type {room_type} not found!")
            return None
        for room, times in self.room_availability[room_type].items():
            if (day, time) in times:
                return room
        return None



    def schedule_session(self, program_year, course_name, session_type, section, day, time):
        if self.check_course_schedule_status(program_year, section, course_name, session_type):
            return False

        room_type = self.courses[course_name].get(session_type)
        if room_type is None:
            return False

        room = self.find_available_room(room_type, day, time)
        if room:
            self.schedule.append((program_year, section, course_name, session_type, day, time, room))
            self.room_availability[room_type][room].remove((day, time))
            self.section_availability[program_year][section].remove((day, time))
            self.update_course_schedule_status(program_year, section, course_name, session_type)
            return True
        return False

    def generate_schedule(self):
        for program_year, sections in self.sections.items():
            for section in sections.keys():
                for course_name in self.courses:
                    for session_type in ['lectures', 'TD', 'TP']:
                        if not self.course_schedule_status[course_name][session_type]:
                            best_option = self.find_best_room_and_time(program_year, course_name, session_type, section)
                            if best_option:
                                day, time, room = best_option
                                self.schedule_session(program_year, course_name, session_type, section, day, time)

    def find_best_room_and_time(self, program_year, course_name, session_type, section):
        best_option = None
        best_score = float('inf') 

        
        for day in self.days:
            for time in self.times:

                if self.is_section_available(program_year, section, day, time):

                    room = self.find_available_room(self.courses[course_name].get(session_type), day, time)
                    if room:
                        score = self.days.index(day) * 100 + self.times.index(time)
                        
                        # If this option is better than previous ones, select it
                        if score < best_score:
                            best_score = score
                            best_option = (day, time, room)
        
        return best_option

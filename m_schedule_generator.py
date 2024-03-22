class ScheduleGenerator:
    
    def __init__(self, rooms, days, times, courses, sections):
        self.rooms = rooms
        self.days = days
        self.times = times
        self.courses = courses
        self.sections = sections
        self.schedule = []

        self.room_availability = {}
        for room_type, room_infos in rooms.items():
            self.room_availability[room_type] = {}
            for room_info in room_infos:
                room_name = room_info['name']
                self.room_availability[room_type][room_name] = [
                    (availability[0], availability[1]) for availability in room_info['availability']
                ]
        self.section_availability = {}
        for program_year, sects in sections.items():
            self.section_availability[program_year] = {}
            for section, groups in sects.items():
                self.section_availability[program_year][section] = [(day, time) for day in days for time in times]


    def find_available_room(self, room_type, day, time):
        for room, available_times in self.room_availability[room_type].items():
            if (day, time) in available_times:
                return room

        return None

    def is_section_available(self, program_year, section, day, time, session_type):
        if session_type == "lectures":
            return all((day, time) in self.section_availability[program_year][sec]
                    for sec in self.sections[program_year])
        return (day, time) in self.section_availability[program_year][section]


    def mark_section_unavailable(self, program_year, section, day, time, session_type):
        if session_type == "lectures":
            for sec in self.section_availability[program_year]:
                if (day, time) in self.section_availability[program_year][sec]:
                    self.section_availability[program_year][sec].remove((day, time))
        else:
            if (day, time) in self.section_availability[program_year][section]:
                self.section_availability[program_year][section].remove((day, time))


    def schedule_session(self, program_year, course_name, session_type, section, day, time):

        if not self.is_section_available(program_year, section, day, time, session_type):
            return False
        
        room_type = self.courses[course_name].get(session_type)
        if room_type:
            available_room = self.find_available_room(room_type, day, time)
            if available_room:
                self.schedule.append((program_year, day, time, course_name, session_type, section, available_room))
                self.room_availability[room_type][available_room].remove((day, time))
                self.mark_section_unavailable(program_year, section, day, time, session_type)
                return True
        return False


    def generate_schedule(self):
        scheduled_sessions = {}
        for program_year, sections in self.sections.items():
            scheduled_sessions[program_year] = {}
            for section, groups in sections.items():
                scheduled_sessions[program_year][section] = {
                    course: {"lectures": False, "TD": False, "TP": False}
                    for course in self.courses
                }

                for course_name, sessions in self.courses.items():
                    for session_type in sessions:
                        if sessions[session_type] is None:
                            continue
                        if session_type == "lectures":
                            for day in self.days:
                                for time in self.times:
                                    if self.is_section_available(program_year, section, day, time, session_type):
                                        available_room = self.find_available_room(sessions[session_type], day, time)
                                        if available_room:
                                            self.schedule.append((program_year, day, time, course_name, session_type, section, available_room))
                                            self.mark_section_unavailable(program_year, section, day, time, session_type)
                                            scheduled_sessions[program_year][section][course_name]["lectures"] = True
                                            break
                                if self.schedule_session(program_year, course_name, session_type, section, day, time):
                                    break

        return scheduled_sessions

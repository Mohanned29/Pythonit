class ScheduleGenerator:
    
    def __init__(self, rooms, days, times, courses, sections):
        self.rooms = rooms
        self.days = days
        self.times = times
        self.courses = courses
        self.sections = sections
        self.schedule = []
        
        #initialiser une salle availability based on actual availability data
        self.room_availability = {} #this dictionary is used to store the availability of rooms based on their type
        for room_type, room_infos in rooms.items(): #rooms heda is a dictionary , keys are type of room , and values are lists (check json file)
            self.room_availability[room_type] = {}
            for room_info in room_infos:
                room_name = room_info['name'] #the room's name is extracted from the room_info dictionary
                #change availability list of lists to list of tuples for consistency and hashability
                self.room_availability[room_type][room_name] = [
                    (availability[0], availability[1]) for availability in room_info['availability']
                ]
        
        #initialize une section availability
        self.section_availability = {section: [(day, time) for day in days for time in times] for section in sections}

    def find_available_room(self, room_type, day, time):
        for room, available_times in self.room_availability[room_type].items():
            if (day, time) in available_times:
                return room

        return None

    def is_section_available(self, section, day, time, session_type):
        if session_type == "lectures":
            return all((day, time) in self.section_availability[section] for section in self.sections)
        return (day, time) in self.section_availability[section]

    def mark_section_unavailable(self, section, day, time, session_type):
        if session_type == "lectures":
            for s in self.sections:
                if (day, time) in self.section_availability[s]:
                    self.section_availability[s].remove((day, time))
        else:
            if (day, time) in self.section_availability[section]:
                self.section_availability[section].remove((day, time))

    def schedule_session(self, course_name, session_type, section_group, day, time):
        section = section_group if session_type == "lectures" else section_group.split()[0]
        if not self.is_section_available(section, day, time, session_type):
            return False
        
        room_type = self.courses[course_name].get(session_type)
        if room_type:
            available_room = self.find_available_room(room_type, day, time)
            if available_room:
                self.schedule.append((day, time, course_name, session_type, section_group, available_room))
                self.room_availability[room_type][available_room].remove((day, time))
                self.mark_section_unavailable(section, day, time, session_type)
                return True
        return False

    def generate_schedule(self):
      scheduled_sessions = {}  #tracker scheduled seances to ensure each occurs once per section/group

      for section in self.sections:
          scheduled_sessions[section] = {course: {"lectures": False, "TD": False, "TP": False} for course in self.courses}
          for group in self.sections[section]:
              for course in scheduled_sessions[section]:
                  if group not in scheduled_sessions[section][course]:
                      scheduled_sessions[section][course][group] = {"TD": False, "TP": False}

      for course_name, sessions in self.courses.items():
        for session_type in sessions:
            if sessions[session_type] is None:
                continue
            for section, groups in self.sections.items():
                if session_type == "lectures" and not scheduled_sessions[section][course_name][session_type]:
                    for day in self.days:
                        session_scheduled = False
                        for time in self.times:
                            if self.schedule_session(course_name, session_type, section, day, time):
                                scheduled_sessions[section][course_name][session_type] = True
                                session_scheduled = True
                                break  #break after scheduling to avoid multiple sessions
                        if session_scheduled:
                            break  #confirmiw beli mykonch 3ndna 2 cour mn nefs el module
                else:  #pour les td et les tp
                    for group in groups:
                        if not scheduled_sessions[section][course_name].get(group, {}).get(session_type, False):
                            session_scheduled = False
                            for day in self.days:
                                for time in self.times:
                                    if self.schedule_session(course_name, session_type, f"{section} {group}", day, time):
                                        scheduled_sessions[section][course_name][group][session_type] = True
                                        session_scheduled = True
                                        break  #schedule only one session per group , chaque grp y9ra cour,td,tp whd mn kol module f smana
                                if session_scheduled:
                                    break #roh lel next group after scheduling
import random

class ScheduleGenerator:
    def __init__(self, rooms, days, times, courses, sections):
        self.rooms = rooms
        self.days = days
        self.times = times
        self.courses = courses
        self.sections = sections
        self.global_room_schedule = {}
        self.session_to_room_type_map = {
            'lecture': 'Amphi',
            'TD': 'TD Room',
            'TP': 'TP Room'
        }
        self.initialize_availability()

    def initialize_availability(self):
        self.room_availability = {}
        for room_type, room_list in self.rooms.items():
            for room_info in room_list:
                room_name = room_info['name']
                self.room_availability[room_name] = {
                    'availability': set((day, time) for day, time in room_info['availability']),
                    'sessions': [],
                }

        self.section_availability = {}
        for section, details in self.sections.items():
            self.section_availability[section] = set((d, t) for d in self.days for t in self.times)

    def is_section_available(self, section, day, time):
        return (day, time) in self.section_availability[section]

    def find_available_room(self, session_type, day, time, global_room_schedule):
        room_type = self.session_to_room_type_map.get(session_type)
        if not room_type:
            print(f"No valid room type mapping found for session type: {session_type}")
            return None

        for room_info in self.rooms.get(room_type, []):
            room_name = room_info['name']
            if (room_name, day, time) not in global_room_schedule:
                # Improved logging to understand room selection failures.
                print(f"Room {room_name} of type {room_type} is available for {session_type} on {day} at {time}")
                return room_name

        print(f"No available room found for {session_type} on {day} at {time} within type {room_type}")
        return None

    def schedule_session(self, course_name, session_type, section, day, time, room, global_room_schedule):
        if room and (room, day, time) not in global_room_schedule:
            # Booking the room in the global schedule
            global_room_schedule[(room, day, time)] = f"{section} - {course_name} - {session_type}"
            print(f"Successfully scheduled {course_name} {session_type} for {section} on {day} at {time} in {room}")
            return True
        else:
            print(f"Failed to book {room} for {course_name} {session_type} on {day} at {time} due to conflict or unavailability.")
            return False

    def generate_schedule(self, global_room_schedule):
        all_schedules = {}
        for section in self.sections:
            section_schedule = []
            # Track which sessions have been scheduled to prevent duplicates
            scheduled_sessions = set()

            for course_name, session_types in self.courses.items():
                for session_type in session_types:
                    session_key = f"{course_name} {session_type}"

                    if session_key not in scheduled_sessions:
                        for day in self.days:
                            for time in self.times:
                                if self.is_section_available(section, day, time):
                                    room = self.find_available_room(session_type, day, time, global_room_schedule)
                                    if room:
                                        scheduled = self.schedule_session(course_name, session_type, section, day, time, room, global_room_schedule)
                                        if scheduled:
                                            section_schedule.append((day, time, room, course_name, session_type))
                                            scheduled_sessions.add(session_key)
                                            # Break out of the innermost loop after scheduling a session
                                            break
                            if session_key in scheduled_sessions:
                                # Break out of the day loop if session is scheduled
                                break
            
            all_schedules[section] = section_schedule
        
        return all_schedules

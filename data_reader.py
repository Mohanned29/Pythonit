import json
import csv

class DataReader:
    @staticmethod
    def read_json_file(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def read_courses_csv(filename):
        courses = {}
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                courses[row['course_name']] = {
                    "lectures": row['lectures'] if row['lectures'] else None,
                    "TD": row['TD'] if row['TD'] else None,
                    "TP": row['TP'] if row['TP'] else None,
                }
        return courses
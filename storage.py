"""storage.py - Load and save student data as JSON."""

import json
import os

from student import Student

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DATA_FILE = os.path.join(DATA_DIR, "students.json")


def load_students(path=DATA_FILE):
    """Return {student_id: Student}. Returns {} if the file is missing/empty/corrupt."""
    students = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        return students                 # first run: no file yet
    except json.JSONDecodeError:
        print("Warning: data file is corrupted. Starting with an empty list.")
        return students

    for item in raw:
        try:
            student = Student.from_dict(item)
        except KeyError as err:
            print(f"Skipping a bad record (missing {err}).")
        else:
            students[student.student_id] = student
    return students


def save_students(students, path=DATA_FILE):
    """Write all students to the JSON file. Returns True on success."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in students.values()], f, indent=4)
    except OSError as err:
        print(f"Error: could not save data ({err}).")
        return False
    return True

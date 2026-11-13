"""student.py - Student class and student-management helpers."""

import re
from datetime import datetime

# Regular expression: 2-4 letters followed by 3-5 digits, e.g. STU001
ID_PATTERN = re.compile(r"^[A-Z]{2,4}\d{3,5}$")
VALID_GENDERS = ("M", "F")


class Student:
    """Represents one student and their subject scores."""

    def __init__(self, student_id, name, class_name, gender, dob,
                 scores=None, date_entered=None):
        self.student_id = student_id
        self.name = name
        self.class_name = class_name
        self.gender = gender
        self.dob = dob                      # string "YYYY-MM-DD"
        self.scores = scores or {}          # {"Mathematics": 78.0, ...}
        self.date_entered = date_entered    # when the result was last entered

    # ----- score helpers -------------------------------------------------
    def set_scores(self, scores):
        """Store scores and stamp the date/time the result was entered."""
        self.scores = dict(scores)
        self.date_entered = datetime.now().strftime("%Y-%m-%d %H:%M")

    def total(self):
        return sum(self.scores.values())

    def average(self):
        if not self.scores:
            return 0.0
        return self.total() / len(self.scores)

    def has_scores(self):
        return bool(self.scores)

    # ----- (de)serialisation --------------------------------------------
    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "class_name": self.class_name,
            "gender": self.gender,
            "dob": self.dob,
            "scores": self.scores,
            "date_entered": self.date_entered,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["student_id"],
            data["name"],
            data["class_name"],
            data["gender"],
            data["dob"],
            data.get("scores", {}),
            data.get("date_entered"),
        )

    def __str__(self):
        return (f"{self.student_id:<9} {self.name:<25} {self.class_name:<8} "
                f"{self.gender:<3} {self.dob}")


# ----- validation --------------------------------------------------------
def valid_id(student_id):
    return bool(ID_PATTERN.match(student_id))


def valid_dob(dob):
    """True if dob is a real date in YYYY-MM-DD format and not in the future."""
    try:
        parsed = datetime.strptime(dob, "%Y-%m-%d")
    except ValueError:
        return False
    return parsed <= datetime.now()


# ----- student management functions (operate on a dict {id: Student}) ----
def add_student(students, student):
    """Add a student. Raises ValueError if the ID already exists."""
    if student.student_id in students:
        raise ValueError(f"Student ID {student.student_id} already exists.")
    students[student.student_id] = student


def find_student(students, query):
    """Search by exact ID or by part of the name. Returns a list of matches."""
    query = query.strip().upper()
    if query in students:
        return [students[query]]
    return [s for s in students.values() if query.lower() in s.name.lower()]


def update_student(students, student_id, **changes):
    """Update fields (name, class_name, gender, dob) of an existing student."""
    student = students.get(student_id)
    if student is None:
        raise KeyError(f"No student with ID {student_id}.")
    for field, value in changes.items():
        if value:                       # empty value means "keep current"
            setattr(student, field, value)
    return student


def delete_student(students, student_id):
    """Delete a student. Raises KeyError if not found."""
    if student_id not in students:
        raise KeyError(f"No student with ID {student_id}.")
    del students[student_id]

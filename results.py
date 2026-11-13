"""results.py - Score validation, grading and ranking logic."""

# Subjects every student is scored in (at least five are required)
SUBJECTS = ["Mathematics", "English", "Physics", "Chemistry", "Biology"]

# (minimum average, grade, remark) - checked from the top down
GRADE_SCALE = [
    (70, "A", "Excellent"),
    (60, "B", "Very Good"),
    (50, "C", "Good"),
    (45, "D", "Pass"),
    (0,  "F", "Fail"),
]


def validate_score(value):
    """Convert text to a float between 0 and 100. Raises ValueError if bad."""
    score = float(value)                # ValueError if not a number
    if not 0 <= score <= 100:
        raise ValueError("Score must be between 0 and 100.")
    return score


def get_grade(average):
    """Return (grade, remark) for an average score."""
    for minimum, grade, remark in GRADE_SCALE:
        if average >= minimum:
            return grade, remark
    return "F", "Fail"


def scored_students(students):
    """Only the students who already have scores recorded."""
    return [s for s in students.values() if s.has_scores()]


def sort_by_average(student_list, descending=True):
    return sorted(student_list, key=lambda s: s.average(), reverse=descending)


def sort_by_name(student_list):
    return sorted(student_list, key=lambda s: s.name.lower())


def class_statistics(student_list):
    """Return a dict of class statistics, or None if there is no data.

    highest/lowest refer to individual subject scores; the top and bottom
    students are found using their averages.
    """
    if not student_list:
        return None

    all_scores = []
    for s in student_list:
        all_scores.extend(s.scores.values())

    averages = [s.average() for s in student_list]
    top = max(student_list, key=lambda s: s.average())
    bottom = min(student_list, key=lambda s: s.average())

    return {
        "count": len(student_list),
        "highest_score": max(all_scores),
        "lowest_score": min(all_scores),
        "class_average": sum(averages) / len(averages),
        "top_student": top,
        "bottom_student": bottom,
    }

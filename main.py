"""main.py - Entry point and menu for the Student Result Management System."""

import storage
import reports
from results import (SUBJECTS, validate_score, scored_students,
                     sort_by_average, sort_by_name)
from student import (Student, valid_id, valid_dob, VALID_GENDERS,
                     add_student, find_student, update_student, delete_student)


# ----- input helpers -----------------------------------------------------
def ask(prompt, validator=None, error="Invalid input.", transform=str.strip):
    """Keep asking until the input passes the validator."""
    while True:
        value = transform(input(prompt))
        if validator is None or validator(value):
            return value
        print(error)


def pick_student(students):
    """Ask for an ID and return the Student, or None if not found."""
    student_id = input("Enter Student ID: ").strip().upper()
    student = students.get(student_id)
    if student is None:
        print("No student with that ID.")
    return student


def read_scores(existing=None):
    """Prompt for a score in every subject. Blank keeps the existing score."""
    scores = {}
    for subject in SUBJECTS:
        old = existing.get(subject) if existing else None
        hint = f" [{old}]" if old is not None else ""
        while True:
            raw = input(f"  {subject}{hint}: ").strip()
            if raw == "" and old is not None:
                scores[subject] = old
                break
            try:
                scores[subject] = validate_score(raw)
            except ValueError as err:
                print(f"  Invalid: {err if 'between' in str(err) else 'enter a number'}")
            else:
                break
    return scores


# ----- menu actions ------------------------------------------------------
def do_add_student(students):
    print("\n-- Add New Student --")
    student_id = ask("Student ID (e.g. STU001): ", valid_id,
                     "ID must be 2-4 letters then 3-5 digits (e.g. STU001).",
                     transform=lambda x: x.strip().upper())
    if student_id in students:
        print("That ID already exists.")
        return
    name = ask("Full name: ", lambda x: len(x) >= 3, "Name is too short.")
    class_name = ask("Class/Form (e.g. SS1): ", lambda x: x != "", "Required.")
    gender = ask("Gender (M/F): ", lambda x: x in VALID_GENDERS,
                 "Enter M or F.", transform=lambda x: x.strip().upper())
    dob = ask("Date of birth (YYYY-MM-DD): ", valid_dob,
              "Use a real past date in YYYY-MM-DD format.")
    try:
        add_student(students, Student(student_id, name, class_name, gender, dob))
    except ValueError as err:
        print(err)
    else:
        print("Student added.")


def do_view_students(students):
    print("\n-- All Students --")
    if not students:
        print("No students registered yet.")
        return
    print(f"{'ID':<9} {'Name':<25} {'Class':<8} {'Sex':<3} DOB")
    for s in sort_by_name(list(students.values())):
        print(s)


def do_search(students):
    query = input("Enter ID or part of a name: ")
    matches = find_student(students, query)
    if not matches:
        print("No match found.")
    for s in matches:
        print(s)


def do_update_student(students):
    student = pick_student(students)
    if not student:
        return
    print("Press Enter to keep the current value.")
    name = input(f"Name [{student.name}]: ").strip()
    class_name = input(f"Class [{student.class_name}]: ").strip()
    gender = input(f"Gender [{student.gender}]: ").strip().upper()
    dob = input(f"DOB [{student.dob}]: ").strip()
    if gender and gender not in VALID_GENDERS:
        print("Gender must be M or F. Update cancelled.")
        return
    if dob and not valid_dob(dob):
        print("Invalid date. Update cancelled.")
        return
    update_student(students, student.student_id, name=name,
                   class_name=class_name, gender=gender, dob=dob)
    print("Student updated.")


def do_delete_student(students):
    student = pick_student(students)
    if not student:
        return
    if input(f"Delete {student.name}? (y/n): ").strip().lower() == "y":
        delete_student(students, student.student_id)
        print("Student deleted.")
    else:
        print("Cancelled.")


def do_record_scores(students):
    student = pick_student(students)
    if not student:
        return
    print(f"Enter scores (0-100) for {student.name}:")
    student.set_scores(read_scores())
    print("Scores recorded.")


def do_update_scores(students):
    student = pick_student(students)
    if not student:
        return
    if not student.has_scores():
        print("No scores yet. Use 'Record scores' first.")
        return
    print("Press Enter to keep a score.")
    student.set_scores(read_scores(student.scores))
    print("Scores updated.")


def do_report_card(students):
    student = pick_student(students)
    if student:
        print(reports.report_card(student))


def do_list_results(students):
    ranked = scored_students(students)
    if not ranked:
        print("No results recorded yet.")
        return
    choice = input("Sort by (1) average high-low, (2) name: ").strip()
    ranked = sort_by_name(ranked) if choice == "2" else sort_by_average(ranked)
    print(reports.results_table(ranked))


def do_statistics(students):
    print(reports.statistics_text(scored_students(students)))


def do_save_report(students):
    ranked = scored_students(students)
    if not ranked:
        print("No results to report yet.")
        return
    try:
        path = reports.save_text_report(sort_by_average(ranked))
    except OSError as err:
        print(f"Could not save report: {err}")
    else:
        print(f"Report saved to {path}")


MENU = """
===== STUDENT RESULT MANAGEMENT SYSTEM =====
 1. Add student            7. Update scores
 2. View all students      8. Student report card
 3. Search student         9. List results (sorted)
 4. Update student        10. Class statistics
 5. Delete student        11. Save text report
 6. Record scores          0. Save and exit
"""

ACTIONS = {
    "1": do_add_student, "2": do_view_students, "3": do_search,
    "4": do_update_student, "5": do_delete_student, "6": do_record_scores,
    "7": do_update_scores, "8": do_report_card, "9": do_list_results,
    "10": do_statistics, "11": do_save_report,
}


def main():
    students = storage.load_students()
    print(f"Loaded {len(students)} student(s).")
    try:
        while True:
            print(MENU)
            choice = input("Choose an option: ").strip()
            if choice == "0":
                break
            action = ACTIONS.get(choice)
            if action is None:
                print("Invalid option, try again.")
                continue
            action(students)
            storage.save_students(students)     # save after every change
    except (KeyboardInterrupt, EOFError):
        print("\nInterrupted.")
    finally:
        if storage.save_students(students):
            print("Data saved. Goodbye!")


if __name__ == "__main__":
    main()

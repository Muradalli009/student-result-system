"""reports.py - Report card, class list and statistics, text export."""

import os
from datetime import datetime

from results import get_grade, class_statistics

LINE = "=" * 62


def report_card(student):
    """Return a formatted report card string for one student."""
    lines = [LINE,
             "STUDENT REPORT CARD".center(62),
             LINE,
             f"Name   : {student.name}",
             f"ID     : {student.student_id}",
             f"Class  : {student.class_name}",
             f"Gender : {student.gender}",
             f"DOB    : {student.dob}",
             "-" * 62]

    if not student.has_scores():
        lines.append("No scores recorded yet.")
    else:
        lines.append(f"{'Subject':<20}{'Score':>8}")
        for subject, score in student.scores.items():
            lines.append(f"{subject:<20}{score:>8.1f}")
        grade, remark = get_grade(student.average())
        lines += ["-" * 62,
                  f"Total   : {student.total():.1f}",
                  f"Average : {student.average():.2f}",
                  f"Grade   : {grade} ({remark})",
                  f"Result entered on: {student.date_entered}"]
    lines.append(LINE)
    return "\n".join(lines)


def results_table(student_list):
    """Return a table of students with total, average and grade."""
    header = (f"{'#':<4}{'ID':<10}{'Name':<26}{'Class':<8}"
              f"{'Total':>8}{'Avg':>8}{'Grade':>7}")
    lines = [header, "-" * len(header)]
    for position, s in enumerate(student_list, start=1):
        grade, _ = get_grade(s.average())
        lines.append(f"{position:<4}{s.student_id:<10}{s.name:<26}{s.class_name:<8}"
                     f"{s.total():>8.1f}{s.average():>8.2f}{grade:>7}")
    return "\n".join(lines)


def statistics_text(student_list):
    stats = class_statistics(student_list)
    if stats is None:
        return "No results available for statistics."
    return "\n".join([
        "CLASS STATISTICS",
        "-" * 40,
        f"Students with results : {stats['count']}",
        f"Highest subject score : {stats['highest_score']:.1f}",
        f"Lowest subject score  : {stats['lowest_score']:.1f}",
        f"Class average         : {stats['class_average']:.2f}",
        f"Best student          : {stats['top_student'].name} "
        f"({stats['top_student'].average():.2f})",
        f"Weakest student       : {stats['bottom_student'].name} "
        f"({stats['bottom_student'].average():.2f})",
    ])


def save_text_report(student_list, filename=None, folder="reports"):
    """Save the full class report to a .txt file. Returns the file path."""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = filename or f"class_report_{stamp}.txt"
    base = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(base, folder)
    os.makedirs(folder_path, exist_ok=True)
    path = os.path.join(folder_path, filename)

    content = "\n\n".join([
        LINE + "\n" + "CLASS RESULT REPORT".center(62) + "\n"
        + f"Generated: {datetime.now():%Y-%m-%d %H:%M}".center(62) + "\n" + LINE,
        results_table(student_list),
        statistics_text(student_list),
    ])
    with open(path, "w", encoding="utf-8") as f:
        f.write(content + "\n")
    return path

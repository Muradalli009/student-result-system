# Student Result Management System

A menu-driven Python application for managing student records, scores and
results. Built for the New Horizon *Introduction to Python Programming*
practical project.

**Author:** Alli Muhammad Ayomide

## Features

- **Student management:** add, view, search (by ID or name), update, delete
- **Results:** record scores for 5 subjects, total, average, grade (A–F), update scores, report card
- **Reports:** list all results, sort by average or name, class statistics, save a text report
- **Persistence:** data saved to `data/students.json` and loaded on start-up (a missing file is handled)
- **Validation:** regex-checked Student IDs, real dates of birth, scores limited to 0–100

## How to run

Requires Python 3.8+ and nothing else (standard library only).

```bash
git clone https://github.com/<your-username>/student-result-system.git
cd student-result-system
python main.py        # use python3 on Mac/Linux
```

A few sample students are included in `data/students.json`. Delete that file to start fresh.

## Project structure

```
student_result_system/
├── main.py       # entry point and menu
├── student.py    # Student class + add/find/update/delete + validation
├── results.py    # subjects, grading, sorting, class statistics
├── storage.py    # load/save JSON
├── reports.py    # report card, tables, text report export
├── data/
│   └── students.json
└── README.md
```

## Grading scale

| Average | Grade | Remark    |
|---------|-------|-----------|
| 70–100  | A     | Excellent |
| 60–69   | B     | Very Good |
| 50–59   | C     | Good      |
| 45–49   | D     | Pass      |
| 0–44    | F     | Fail      |

## Python concepts used

| Concept | Where |
|---|---|
| Variables, types, type conversion | `float()` conversion of scores in `results.validate_score` |
| Flow control | `if/elif/else`, `for`, `while` input loops in `main.py` |
| Lists, tuples, dictionaries | students stored as `{id: Student}`; `GRADE_SCALE` is a list of tuples |
| Functions | every module, with parameters and return values |
| Sorting | `sorted()` with `key=lambda` in `results.py` |
| Exception handling | `try/except/else/finally` in `storage.py` and `main.py` |
| File handling | JSON read/write in `storage.py`; text report in `reports.py` |
| Modules and packages | five `.py` files |
| OOP | `Student` class with methods, `to_dict` / `from_dict` |
| Dates and times | `datetime` stamps when a result is entered; DOB validation |
| Standard library | `json`, `os`, `re`, `datetime` |
| Regular expressions | Student ID format `^[A-Z]{2,4}\d{3,5}$` |

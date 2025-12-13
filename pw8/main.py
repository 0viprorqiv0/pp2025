import curses
import math
import numpy as np

from domains import Student, Course, Mark
from input import curses_input
from output import draw_table, show_message
import storage


class StudentMarkSystem:
    def __init__(self):
        self.students = []
        self.courses = []
        self.marks = []
        if storage.dat_exists():
            storage.decompress()
            self.students, self.courses, self.marks = storage.load_pickle()
        self.persist = storage.BackgroundPersistence(method="gz")
    def _autosave(self):
        self.persist.notify_save(self.students, self.courses, self.marks)
        
    def add_student_ui(self, stdscr):
        sid = curses_input(stdscr, "Student ID:")
        name = curses_input(stdscr, "Student Name:")
        dob = curses_input(stdscr, "DoB:")
        self.students.append(Student(sid, name, dob))
        self._autosave()

    def add_course_ui(self, stdscr):
        cid = curses_input(stdscr, "Course ID:")
        name = curses_input(stdscr, "Course Name:")
        credits = float(curses_input(stdscr, "Credits:"))
        self.courses.append(Course(cid, name, credits))
        self._autosave()
        
    def input_mark_ui(self, stdscr):
        if not self.students or not self.courses:
            show_message(stdscr, "Need students and courses first.")
            return

        cid = curses_input(stdscr, "Course ID:")
        for s in self.students:
            raw = float(curses_input(stdscr, f"Mark for {s.name}:"))
            val = math.floor(raw * 10) / 10
            self.marks.append(Mark(s.id, cid, val))
        self._autosave()

    def show_students_ui(self, stdscr):
        rows = [f"{s.id} - {s.name} - GPA {round(s.gpa,2)}" for s in self.students]
        draw_table(stdscr, "STUDENTS", rows)

    def show_courses_ui(self, stdscr):
        rows = [f"{c.id} - {c.name} - {c.credits}" for c in self.courses]
        draw_table(stdscr, "COURSES", rows)

    def show_marks_ui(self, stdscr):
        cid = curses_input(stdscr, "Course ID:")
        rows = []
        for s in self.students:
            score = next((m.value for m in self.marks if m.student_id == s.id and m.course_id == cid), "N/A")
            rows.append(f"{s.name} - {score}")
        draw_table(stdscr, "MARKS", rows)

    def calc_gpa(self):
        for s in self.students:
            ms, cs = [], []
            for m in self.marks:
                if m.student_id == s.id:
                    for c in self.courses:
                        if c.id == m.course_id:
                            ms.append(m.value)
                            cs.append(c.credits)
            s.gpa = float(np.sum(np.array(ms)*np.array(cs))/np.sum(cs)) if ms else 0.0

    def run(self):
        curses.wrapper(self.menu)

    def menu(self, stdscr):
        menu = ["Add Student", "Add Course", "Input Marks", "Show Students", "Show Courses", "Show Marks", "Calculate GPA", "Exit"]
        cur = 0

        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            stdscr.addstr(1, w//2 - 8, "USTH SYSTEM (PW8)")

            for i, m in enumerate(menu):
                y = h//2 - len(menu)//2 + i
                x = w//2 - len(m)//2
                if i == cur:
                    stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, m)
                stdscr.attroff(curses.A_REVERSE)

            k = stdscr.getch()
            if k == curses.KEY_UP:
                cur = (cur - 1) % len(menu)
            elif k == curses.KEY_DOWN:
                cur = (cur + 1) % len(menu)
            elif k in (10, 13):
                if cur == 0: self.add_student_ui(stdscr)
                elif cur == 1: self.add_course_ui(stdscr)
                elif cur == 2: self.input_mark_ui(stdscr)
                elif cur == 3: self.show_students_ui(stdscr)
                elif cur == 4: self.show_courses_ui(stdscr)
                elif cur == 5: self.show_marks_ui(stdscr)
                elif cur == 6:
                    self.calc_gpa()
                    show_message(stdscr, "GPA calculated")
                elif cur == 7:
                    method = curses_input(stdscr, "Compression (gz/none):").strip().lower()
                    if method not in ("gz", "none"):
                        method = "gz"

                    self.persist.method = method
                    self._autosave()
                    self.persist.close()
                    break


if __name__ == "__main__":
    StudentMarkSystem().run()

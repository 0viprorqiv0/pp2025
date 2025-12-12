import curses
from curses import textpad
import numpy as np
import math

class Student:
    def __init__(self, sid, name, dob):
        self.id = sid
        self.name = name
        self.dob = dob
        self.gpa = 0.0

class Course:
    def __init__(self, cid, name, credits):
        self.id = cid
        self.name = name
        self.credits = credits


class Mark:
    def __init__(self, student_id, course_id, value):
        self.student_id = student_id
        self.course_id = course_id
        self.value = value


def curses_input(stdscr, prompt):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    stdscr.addstr(h // 2 - 2, w // 2 - len(prompt) // 2, prompt)

    edit_win = curses.newwin(1, 30, h // 2, w // 2 - 15)
    textpad.rectangle(stdscr, h // 2 - 1, w // 2 - 16, h // 2 + 1, w // 2 + 14)
    stdscr.refresh()

    box = textpad.Textbox(edit_win)
    content = box.edit().strip()
    return content


def draw_table(stdscr, title, rows):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    stdscr.addstr(1, w // 2 - len(title) // 2, title)

    y = 3
    for row in rows:
        stdscr.addstr(y, 2, row)
        y += 1

    stdscr.addstr(h - 2, 2, "Press any key to return...")
    stdscr.refresh()
    stdscr.getch()

class StudentMarkSystem:
    def __init__(self):
        self.students = []
        self.courses = []
        self.marks = []

    def add_student_ui(self, stdscr):
        sid = curses_input(stdscr, "Enter Student ID:")
        name = curses_input(stdscr, "Enter Student Name:")
        dob = curses_input(stdscr, "Enter DoB (dd/mm/yyyy):")

        self.students.append(Student(sid, name, dob))

    def add_course_ui(self, stdscr):
        cid = curses_input(stdscr, "Enter Course ID:")
        name = curses_input(stdscr, "Enter Course Name:")
        credits = float(curses_input(stdscr, "Enter Credits:"))

        self.courses.append(Course(cid, name, credits))

    def show_students_ui(self, stdscr):
        rows = [
            f"{s.id} - {s.name} - {s.dob} - GPA: {round(s.gpa, 2)}"
            for s in self.students
        ]
        draw_table(stdscr, "STUDENT LIST", rows)

    def show_courses_ui(self, stdscr):
        rows = [
            f"{c.id} - {c.name} - {c.credits} credits"
            for c in self.courses
        ]
        draw_table(stdscr, "COURSE LIST", rows)

    def input_mark_ui(self, stdscr):
        if not self.students or not self.courses:
            stdscr.clear()
            stdscr.addstr(2, 2, "Need students and courses first.")
            stdscr.addstr(4, 2, "Press any key to return...")
            stdscr.refresh()
            stdscr.getch()
            return

        cid = curses_input(stdscr, "Enter Course ID to input marks:")

        for s in self.students:
            prompt = f"Mark for {s.id} - {s.name}:"
            raw = float(curses_input(stdscr, prompt))

            val = math.floor(raw * 10) / 10

            self.marks.append(Mark(s.id, cid, val))

    def show_marks_ui(self, stdscr):
        cid = curses_input(stdscr, "Enter Course ID:")
        rows = []

        for s in self.students:
            score = next(
                (m.value for m in self.marks if m.student_id == s.id and m.course_id == cid),
                "N/A"
            )
            rows.append(f"{s.id} - {s.name} - {score}")

        draw_table(stdscr, f"MARKS FOR COURSE {cid}", rows)

    def calc_gpa(self):
        for s in self.students:
            marks_arr = []
            credits_arr = []

            for m in self.marks:
                if m.student_id == s.id:
                    for c in self.courses:
                        if c.id == m.course_id:
                            marks_arr.append(m.value)
                            credits_arr.append(c.credits)

            if marks_arr:
                m_np = np.array(marks_arr)
                c_np = np.array(credits_arr)
                s.gpa = float(np.sum(m_np * c_np) / np.sum(c_np))
            else:
                s.gpa = 0.0

    def sort_gpa(self):
        self.calc_gpa()
        self.students.sort(key=lambda x: x.gpa, reverse=True)

    def run(self):
        curses.wrapper(self._menu)

    def _menu(self, stdscr):
        curses.curs_set(0)

        menu = [
            "Add Student",
            "Add Course",
            "Input Marks",
            "Show Marks",
            "Show Students",
            "Show Courses",
            "Calculate GPA",
            "Sort by GPA",
            "Exit",
        ]

        current = 0

        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()

            stdscr.addstr(1, w // 2 - len("USTH MARK SYSTEM") // 2, "USTH MARK SYSTEM")

            for i, row in enumerate(menu):
                x = w // 2 - len(row) // 2
                y = h // 2 - len(menu) // 2 + i

                if i == current:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(y, x, row)
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(y, x, row)

            key = stdscr.getch()

            if key == curses.KEY_UP:
                current = (current - 1) % len(menu)
            elif key == curses.KEY_DOWN:
                current = (current + 1) % len(menu)
            elif key in (10, 13):  # Enter
                choice = current

                if choice == 0:
                    self.add_student_ui(stdscr)
                elif choice == 1:
                    self.add_course_ui(stdscr)
                elif choice == 2:
                    self.input_mark_ui(stdscr)
                elif choice == 3:
                    self.show_marks_ui(stdscr)
                elif choice == 4:
                    self.show_students_ui(stdscr)
                elif choice == 5:
                    self.show_courses_ui(stdscr)
                elif choice == 6:
                    self.calc_gpa()
                elif choice == 7:
                    self.sort_gpa()
                elif choice == 8:
                    break

            stdscr.refresh()


if __name__ == "__main__":
    sms = StudentMarkSystem()
    sms.run()

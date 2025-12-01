class Student:
    def __init__(self, sid, name, dob):
        self.id = sid
        self.name = name
        self.dob = dob
        
class Course:
    def __init__(self, cid, name):
        self.id = cid
        self.name = name
        
class Mark:
    def __init__(self, student_id, course_id, value):
        self.student_id = student_id
        self.course_id = course_id
        self.value = value

class StudentMarkSystem:
    def __init__(self):
        self.students = []
        self.courses = []
        self.marks = []
        
    def add_student(self, sid, name, dob):
        self.students.append(Student(sid, name, dob))
    
    def input_students(self):
        n = int(input("Number of students: "))
        for _ in range(n):
            sid = input("Student ID: ")
            name = input("Name: ")
            dob = input("DoB: ")
            self.add_student(sid, name, dob)
            
    def list_students(self):
        print("\nStudents:")
        for s in self.students:
            print(f"{s.id} - {s.name} - {s.dob}")
            
    def add_course(self, cid, name):
        self.courses.append(Course(cid, name))
        
    def input_courses(self):
        n = int(input("Number of courses: "))
        for _ in range(n):
            cid = input("Course ID: ")
            name = input("Course name: ")
            self.add_course(cid, name)
            
    def list_courses(self):
        print("\nCourses:")
        for c in self.courses:
            print(f"{c.id} - {c.name}")
            
    def input_marks_for_course(self):
        if not self.courses or not self.students:
            print("Need students and courses first.")
            return
        self.list_courses()
        cid = input("Select course ID: ")
        for s in self.students:
            m = float(input(f"Mark for {s.id} - {s.name}: "))
            self.marks.append(Mark(s.id, cid, m))
            
    def show_marks_for_course(self):
        self.list_courses()
        cid = input("Course ID to show marks: ")
        print("\nMarks:")
        for s in self.students:
            mark = None
            for m in self.marks:
                if m.student_id == s.id and m.course_id == cid:
                    mark = m.value
                    break
            mark_value = mark if mark is not None else 'N/A'
            print(f"{s.id} - {s.name} - {mark_value}")
            
    def run(self):
        while True:
            print("\n1. Input students")
            print("2. Input courses")
            print("3. List students")
            print("4. List courses")
            print("5. Input marks for course")
            print("6. Show marks for course")
            print("0. Exit")

            choice = input("Choice: ")

            if choice == "1": self.input_students()
            elif choice == "2": self.input_courses()
            elif choice == "3": self.list_students()
            elif choice == "4": self.list_courses()
            elif choice == "5": self.input_marks_for_course()
            elif choice == "6": self.show_marks_for_course()
            elif choice == "0": break
            else:
                print("Invalid")


if __name__ == "__main__":
    StudentMarkSystem().run()
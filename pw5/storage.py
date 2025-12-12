import os
import tarfile

STUDENTS = "students.txt"
COURSES = "courses.txt"
MARKS = "marks.txt"
DATA = "students.dat"

def write_students(students):
    with open(STUDENTS, "w", encoding = "utf-8") as f:
        for s in students:
            f.write(f"{s.id}|{s.name}|{s.dob}\n")


def write_courses(courses):
    with open(COURSES, "w", encoding = 'utf-8') as f:
        for c in courses:
            f.write(f"{c.id}|{c.name}|{c.credits}\n")
            
def write_marks(marks):
    with open(MARKS, "w", encoding = "utf-8") as f:
        for m in marks:
            f.write(f"{m.student_id}|{m.course_id}|{m.value}\n")
            
def compress(method = "gz"):
    mod = "w:gz" if method == "gz" else "w"
    with tarfile.open(DATA, mode) as tar:
        for f in [STUDENTS, COURSES, MARKS]:
            if os.path.exists(f):
                tar.add(f)
                
def dat_exists():
    return os.path.exists(DATA)

def decompress():
    with tarfile.open(DATA, "r:*") as tar:
        tar.extractall()
        
def load_students(Student):
    res = []
    if not os.path.exists(STUDENTS):
        return res
    with open(STUDENTS, "r", encoding = "utf-8") as f:
        for line in f:
            sid, name, dob, = line.strip().split("|")
            res.append(Student(sid, name, dob))
    return res

def load_courses(Course):
    res = []
    if not os.path.exists(COURSES):
        return res
    with open(COURSES, "r", encoding = "utf-8") as f:
        for line in f:
            cid, name, credits = line.strip().split("|")
            res.append(Course(cid, name, float(credits)))
    return res

def load_marks(Mark):
    res = []
    if not os.path.exists(MARKS):
        return res
    with open(MARKS, "r", encoding = "utf-8") as f:
        for line in f:
            sid, cid, val = line.strip().split("|")
            res.append(Mark(sid, cid, float(val)))
    return res
students = []       
courses = []        
marks = {}          

def input_students():
    n = int(input("Number of students: "))
    for i in range(n):
        sid = input("Student ID: ")
        name = input("Name: ")
        dob = input("DoB: ")
        students.append({"id": sid, "name": name, "dob": dob})

def input_courses():
    n = int(input("Number of courses: "))
    for i in range(n):
        cid = input("Course ID: ")
        name = input("Course name: ")
        courses.append({"id": cid, "name": name})

def list_students():
    print("\nStudents:c")
    for s in students:
        print(s["id"], "-", s["name"], "-", s["dob"])

def list_courses():
    print("\nCourses:")
    for c in courses:
        print(c["id"], "-", c["name"])

def input_marks_for_course():
    list_courses()
    cid = input("Select course ID: ")
    for s in students:
        m = float(input(f"Mark for {s['id']} - {s['name']}: "))
        marks[(s["id"], cid)] = m

def show_marks_for_course():
    list_courses()
    cid = input("Course ID to show marks: ")
    print("\nMarks:")
    for s in students:
        key = (s["id"], cid)
        if key in marks:
            print(s["id"], s["name"], "=>", marks[key])
        else:
            print(s["id"], s["name"], "=> N/A")

while True:
    print("\n1. Input students")
    print("2. Input courses")
    print("3. List students")
    print("4. List courses")
    print("5. Input marks for course")
    print("6. Show marks for course")
    print("0. Exit")

    choice = input("Choice: ")

    if choice == "1": input_students()
    elif choice == "2": input_courses()
    elif choice == "3": list_students()
    elif choice == "4": list_courses()
    elif choice == "5": input_marks_for_course()
    elif choice == "6": show_marks_for_course()
    elif choice == "0": break
    else: print("Invalid.")

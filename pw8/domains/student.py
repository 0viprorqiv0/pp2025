class Student:
    def __init__(self, sid, name, dob):
        self.id = sid
        self.name = name
        self.dob = dob
        self.gpa = 0.0

    def __str__(self):
        return f"Student(id={self.id}, name={self.name}, dob={self.dob}, gpa={self.gpa})"
        

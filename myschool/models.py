class Base:
    def __repr__(self):
        return str(self.__dict__)

class Assignment(Base):
    def __init__(self, id, name, date, course_id):
        self.name = name
        self.date = date
        self.course_id = int(course_id)
        self.id = int(id)

class Course(Base):
    def __init__(self, id, name, course_code, semester_code):
        self.id = int(id)
        self.name = name
        self.course_code = course_code
        self.semester_code = semester_code

class Submission(Base):
    def __init__(self, kt, id, grade, comment):
        self.kt = kt
        self.id = int(id) if id else None
        self.grade = grade
        self.comment = comment

class Student(Base):
    def __init__(self, name, kt, username = None):
        self.name = name
        self.username = username
        self.kt = kt


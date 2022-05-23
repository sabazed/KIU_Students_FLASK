"""
REST API for students and schools of university (KIU)
=====================================================
@Endpoints:
    Getting all schools - "/schools"
    Getting school by id - "/schools/<id>"
    Adding school - "/schools/new"
    Updating school - "/schools/update"
    Deleting school - "/schools/delete"
    Getting all students - "/students"
    Getting students by school - "/students/school/<id>"
    Getting student by id - "/students/<id>"
    Adding student - "/students/new"
    Updating student - "/students/update"
    Deleting student - "/students/delete"
"""

import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uni.sqlite'
db = SQLAlchemy(app)
# First list for checking student parameters, second one for school
param_arr = [["first_name", "last_name", "email", "phone", "gpa", "campus", "school"], ["title", "email", "phone"]]


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    students = db.relationship("Student", backref="course", lazy=True)

    def __repr__(self):
        return f"School('{self.id}, {self.title}', '{self.email}', '{self.phone}')"


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    gpa = db.Column(db.Float, nullable=False)
    campus = db.Column(db.Boolean, nullable=False)
    school = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)

    def __repr__(self):
        return f"(Student[{self.id}] {self.first_name} {self.last_name}, {self.school})"


# If the database doesn't exist it gets created
if not os.path.exists('/uni.sqlite'):
    db.create_all()


@app.route('/students', methods=['GET'])
def get_students_all():
    return str(Student.query.all())


@app.route('/students/school/<int:school_id>/', methods=['GET'])
def get_students_by_school(school_id):
    return str(Student.query.filter_by(school=school_id).all())


@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    return str(Student.query.get(student_id))


@app.route('/students/new/<int:school_id>/', methods=['POST'])
def add_student(school_id):
    inp = request.json
    try:
        student = Student(first_name=inp["first_name"], last_name=inp["last_name"], email=inp["email"],
                          phone=inp["phone"], gpa=inp["gpa"], campus=inp["campus"], school=school_id)
        db.session.add(student)
        db.session.commit()
    except KeyError:
        return "Please fill all necessary keys"
    return f"Student added - {student}"


# Checks if the json provided includes all valid data for adding a new student
def check_student(jsoninput):
    params = param_arr[0]
    for j in jsoninput:
        if j not in params:
            return False
    return True


@app.route('/students/update', methods=['PUT'])
def update_student():
    inp = request.json
    if "id" not in inp:
        if check_student(inp):
            student = Student(first_name=inp["first_name"], last_name=inp["last_name"], email=inp["email"],
                              phone=inp["phone"], gpa=inp["gpa"], campus=inp["campus"], school=inp["school"])
            db.session.add(student)
            db.session.commit()
            return f"New student added - {student}"
        else:
            return "Please provide ID of the student to update data"
    else:
        student = Student.query.get(inp["id"])
        if student is not None:
            if "first_name" in inp:
                student.first_name = inp["first_name"]
            if "last_name" in inp:
                student.last_name = inp["last_name"]
            if "email" in inp:
                student.email = inp["email"]
            if "phone" in inp:
                student.phone = inp["phone"]
            if "gpa" in inp:
                student.gpa = inp["gpa"]
            if "campus" in inp:
                student.campus = inp["campus"]
            if "school" in inp:
                student.school = inp["school"]
            db.session.commit()
            return f"Student info updated - {student}"
        else:
            return f"Please provide a valid ID to update the data"


@app.route('/students/delete', methods=['DELETE'])
def delete_student():
    inp = request.json
    if "id" not in inp:
        return "Please provide ID of the student to delete"
    Student.query.filter_by(id=inp["id"]).delete()
    db.session.commit()
    return f"Student deleted"


# Checks if the json provided includes all valid data for adding a new school
def check_school(jsoninput):
    params = param_arr[1]
    for j in jsoninput:
        if j not in params:
            return False
    return True


@app.route('/schools', methods=['GET'])
def get_schools():
    return str(School.query.all())


@app.route('/schools/<int:school_id>', methods=['GET'])
def get_school(school_id):
    return str(School.query.get(school_id))


@app.route('/schools/new', methods=['POST'])
def add_school():
    inp = request.json
    try:
        school = School(title=inp["title"], email=inp["email"], phone=inp["phone"])
        db.session.add(school)
        db.session.commit()
    except KeyError:
        return "Please fill all necessary keys"
    return f"School added - {school}"


@app.route('/schools/update', methods=['PUT'])
def update_school():
    inp = request.json
    if "id" not in inp:
        if check_school(inp):
            school = School(title=inp["title"], email=inp["email"], phone=inp["phone"])
            db.session.add(school)
            db.session.commit()
            return f"New school added - {school}"
        else:
            return "Please provide ID of the school to update data"
    else:
        school = School.query.get(inp["id"])
        if school is not None:
            if "title" in inp:
                school.title = inp["title"]
            if "email" in inp:
                school.email = inp["email"]
            if "phone" in inp:
                school.phone = inp["phone"]
            db.session.commit()
            return f"School info updated - {school}"
        else:
            return f"Please provide a valid ID to update the data"


@app.route('/schools/delete', methods=['DELETE'])
def delete_school():
    inp = request.json
    if "id" not in inp:
        return "Please provide ID of the student to delete"
    School.query.filter_by(id=inp["id"]).delete()
    db.session.commit()
    return f"School deleted"


if __name__ == '__main__':
    app.run()

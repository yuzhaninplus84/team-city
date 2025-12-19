from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id_student = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    year_of_admission = db.Column(db.Integer, nullable=False)
    form_of_study = db.Column(db.String(20))  # ví dụ: "Full-time", "Part-time"
    education_level = db.Column(db.String(50))
    course_code = db.Column(db.String(20))
    group_number = db.Column(db.String(10))
    number_phone = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)

class Course(db.Model):
    id_course = db.Column(db.String(50), primary_key=True)
    name_course = db.Column(db.String(100), nullable=False)
    total_hours = db.Column(db.Integer, nullable=False)
    number_year = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)

class StudyPlan(db.Model):
    id_plan= db.Column(db.String(50), primary_key=True)
    id_course = db.Column(db.String(50), db.ForeignKey('course.id_course'))
    discipline = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    credit_of_discipline = db.Column(db.Integer, nullable=False)
    exam_format = db.Column(db.String(20), nullable=False)

class StudentProgressLog(db.Model):
    id_log = db.Column(db.Integer, primary_key=True)
    semester = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id_student'))
    course_id = db.Column(db.String(50), db.ForeignKey('course.id_course'))
    grade = db.Column(db.String(20))

# Lab 8.4
from datetime import datetime

class StudentAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id_student'))
    course_id = db.Column(db.String(50), db.ForeignKey('course.id_course'))
    attendance_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Attendance {self.student_id} {self.attendance_date}>'
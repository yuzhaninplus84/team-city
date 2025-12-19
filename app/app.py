from flask import Flask, render_template, request, jsonify
from models import db, Student, Course, StudyPlan, StudentProgressLog, StudentAttendance
from datetime import datetime



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'   # cần cho WTForms
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/")
def home():
    all_plans = StudyPlan.query.all()
    all_course = Course.query.all()
    return render_template("index.html", study_plans=all_plans, courses = all_course)

@app.route("/students")
def students():
    all_students = Student.query.all()
    return render_template("students.html", students = all_students)

@app.route("/study_plan")
def study_plan():
    all_study_plans = StudyPlan.query.all()
    return render_template("studyplan.html", study_plans=all_study_plans)

@app.route("/grades")
def grades():
    all_progress_logs = StudentProgressLog.query.all()
    return render_template("grades.html", progress_logs=all_progress_logs)

@app.route("/course")
def course():
    all_courses = Course.query.all()
    return render_template("course.html", courses=all_courses)

@app.route('/add_student', methods=['POST'])
def add_student():
    try:
        data = request.get_json()  # nhận JSON từ JS
        if not data:
            return jsonify({'success': False, 'message': 'No data received'}), 400

        new_student = Student(
            id_student=data.get('id_student'),
            last_name=data.get('last_name'),
            full_name=data.get('full_name'),
            year_of_admission=data.get('year_of_admission'),
            form_of_study=data.get('form_of_study'),
            education_level=data.get('education_level'),
            course_code=data.get('course_code'),
            group_number=data.get('group_number'),
            number_phone=data.get('number_phone'),
            email=data.get('email')
        )
        db.session.add(new_student)
        db.session.commit()
        return jsonify({'success': True,
                        'student': {
                            'id_student': new_student.id_student,
                            'last_name': new_student.last_name,
                            'full_name': new_student.full_name,
                            'year_of_admission': new_student.year_of_admission,
                            'form_of_study': new_student.form_of_study,
                            'education_level': new_student.education_level,
                            'course_code': new_student.course_code,
                            'group_number': new_student.group_number,
                            'number_phone': new_student.number_phone,
                            'email': new_student.email
                        }})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    
@app.route('/student/<int:id_student>', methods=['GET'])
def get_student(id_student):
    student = Student.query.get(id_student)
    if student:
        return jsonify({
            'id_student': student.id_student,
            'last_name': student.last_name,
            'full_name': student.full_name,
            'year_of_admission': student.year_of_admission,
            'form_of_study': student.form_of_study,
            'education_level': student.education_level,
            'course_code': student.course_code,
            'group_number': student.group_number,
            'number_phone': student.number_phone,
            'email': student.email
        })
    return jsonify({'error': 'Student not found'}), 404

@app.route('/student/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"}), 200

@app.route('/student/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    student.last_name = request.form['last_name']
    student.full_name = request.form['full_name']
    student.year_of_admission = request.form['year_of_admission']
    student.form_of_study = request.form.get('form_of_study')
    student.education_level = request.form.get('education_level')
    student.course_code = request.form.get('course_code')
    student.group_number = request.form.get('group_number')
    student.number_phone = request.form.get('number_phone')
    student.email = request.form.get('email')

    db.session.commit()
    return jsonify({"message": "Student updated successfully"})

@app.route('/add_course', methods=['POST'])
def add_course():
    try:
        data = request.get_json()  # nhận JSON từ JS
        if not data:
            return jsonify({'success': False, 'message': 'No data received'}), 400
        print(data)
        new_course = Course(
            id_course=data.get('id_course'),
            name_course=data.get('name_course'),
            total_hours=data.get('total_hours'),
            number_year=data.get('number_year'),
            description=data.get('description')
        )
        db.session.add(new_course)
        db.session.commit()
        return jsonify({'success': True,
                        'course': {
                            'id_course': new_course.id_course,
                            'name_course': new_course.name_course,
                            'total_hours': new_course.total_hours,
                            'number_year': new_course.number_year,
                            'description': new_course.description
                        }})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/course/<string:id_course>', methods=['GET'])
def get_course(id_course):
    course = Course.query.get(id_course)
    print(course)
    if course:
        return jsonify({
            'id_course': course.id_course,
            'name_course': course.name_course,
            'total_hours': course.total_hours,
            'number_year': course.number_year,
            'description': course.description
        })
    return jsonify({'error': 'Course not found'}), 404



@app.route('/course/<string:id_course>', methods=['DELETE'])
def delete_course(id_course):
    course = Course.query.get_or_404(id_course)
    db.session.delete(course)
    db.session.commit()
    return jsonify({"message": "Course deleted successfully"}), 200

@app.route('/course/<string:id_course>', methods=['PUT'])
def update_course(id_course):
    course = Course.query.get_or_404(id_course)
    course.name_course = request.form['name_course']
    course.total_hours = request.form['total_hours']
    course.number_year = request.form['number_year']
    course.description = request.form.get('description')

    db.session.commit()
    return jsonify({"message": "Course updated successfully"})



@app.route('/add_studyplan', methods=['POST'])
def add_studyplan():
    try:
        data = request.get_json()  # nhận JSON từ JS
        if not data:
            return jsonify({'success': False, 'message': 'No data received'}), 400
        print(data)
        new_studyplan = StudyPlan(
            id_plan=data.get('id_plan'),
            id_course=data.get('id_course'),
            discipline=data.get('discipline'),
            semester=data.get('semester'),
            credit_of_discipline=data.get('credit_of_discipline'),
            exam_format=data.get('exam_format')
        )
        db.session.add(new_studyplan)
        db.session.commit()
        return jsonify({'success': True,
                        'studyplan': {
                            'id_plan': new_studyplan.id_plan,
                            'id_course': new_studyplan.id_course,
                            'discipline': new_studyplan.discipline,
                            'semester': new_studyplan.semester,
                            'credit_of_discipline': new_studyplan.credit_of_discipline,
                            'exam_format': new_studyplan.exam_format
                        }})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/study_plan/<string:id_plan>', methods=['GET'])
def get_study_plan(id_plan):
    study_plan = StudyPlan.query.get(id_plan)
    print(study_plan)
    if study_plan:
        return jsonify({
            'id_plan': study_plan.id_plan,
            'id_course': study_plan.id_course,
            'discipline': study_plan.discipline,
            'semester': study_plan.semester,
            'credit_of_discipline': study_plan.credit_of_discipline,
            'exam_format': study_plan.exam_format
        })
    return jsonify({'error': 'Study plan not found'}), 404

@app.route('/study_plan/<string:id_plan>', methods=['DELETE'])
def delete_study_plan(id_plan):
    study_plan = StudyPlan.query.get_or_404(id_plan)
    db.session.delete(study_plan)
    db.session.commit()
    return jsonify({"message": "Study plan deleted successfully"}), 200

@app.route('/study_plan/<string:id_plan>', methods=['PUT'])
def update_study_plan(id_plan):
    study_plan = StudyPlan.query.get_or_404(id_plan)
    study_plan.id_course = request.form['id_course']
    study_plan.discipline = request.form['discipline']
    study_plan.semester = request.form['semester']
    study_plan.credit_of_discipline = request.form['credit_of_discipline']
    study_plan.exam_format = request.form['exam_format']

    db.session.commit()
    return jsonify({"message": "Study plan updated successfully"})

@app.route('/add_grades', methods=['POST'])
def add_grades():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data received'}), 400

        new_progress_log = StudentProgressLog(
            id_log=data.get('id_log'),
            semester=data.get('semester'),
            student_id=data.get('student_id'),
            course_id=data.get('course_id'),
            grade=data.get('grade')
        )

        db.session.add(new_progress_log)
        db.session.commit()

        return jsonify({'success': True,
                        'progress_log': {
                            'id_log': new_progress_log.id_log,
                            'semester': new_progress_log.semester,
                            'student_id': new_progress_log.student_id,
                            'course_id': new_progress_log.course_id,
                            'grade': new_progress_log.grade
                        }})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/grades/<string:id_log>', methods=['GET'])
def get_progress_log(id_log):
    progress_log = StudentProgressLog.query.get(id_log)
    print(progress_log)
    if progress_log:
        return jsonify({
            'id_log': progress_log.id_log,
            'semester': progress_log.semester,
            'student_id': progress_log.student_id,
            'course_id': progress_log.course_id,
            'grade': progress_log.grade
        })
    return jsonify({'error': 'Progress log not found'}), 404

@app.route('/grades/<string:id_log>', methods=['DELETE'])
def delete_progress_log(id_log):
    progress_log = StudentProgressLog.query.get_or_404(id_log)
    db.session.delete(progress_log)
    db.session.commit()
    return jsonify({"message": "Progress log deleted successfully"}), 200

@app.route('/grades/<string:id_log>', methods=['PUT'])
def update_progress_log(id_log):
    progress_log = StudentProgressLog.query.get_or_404(id_log)
    progress_log.semester = request.form['semester']
    progress_log.student_id = request.form['student_id']
    progress_log.course_id = request.form['course_id']
    progress_log.grade = request.form['grade']

    db.session.commit()
    return jsonify({"message": "Progress log updated successfully"})

@app.route('/students/count/<string:form_of_study>', methods=['GET'])
def count_students_by_form(form_of_study):
    count = Student.query.filter_by(form_of_study=form_of_study).count()
    return jsonify({
        'form_of_study': form_of_study,
        'count': count
    })

@app.route('/course/info/<string:id_plan>', methods=['GET'])
def get_course_info(id_plan):
    plan = StudyPlan.query.get(id_plan)
    if not plan:
        return jsonify({'error': 'Study plan not found'}), 404

    return jsonify({
        'id_plan': plan.id_plan,
        'id_course': plan.id_course,
        'discipline': plan.discipline,
        'semester': plan.semester,
        'credit_of_discipline': plan.credit_of_discipline,
        'exam_format': plan.exam_format
    })

@app.route('/students/group/<string:group_number>', methods=['GET'])
def get_students_by_group(group_number):
    students = Student.query.filter_by(group_number=group_number).all()
    return jsonify([
        {
            'id_student': s.id_student,
            'full_name': s.full_name,
            'group_number': s.group_number,
            'form_of_study': s.form_of_study
        } for s in students
    ])

@app.route('/grades/student/<int:student_id>', methods=['GET'])
def get_student_grades(student_id):
    semester = request.args.get('semester', type=int)
    query = StudentProgressLog.query.filter_by(student_id=student_id)
    if semester:
        query = query.filter_by(semester=semester)
    grades = query.all()

    return jsonify([
        {
            'id_log': g.id_log,
            'semester': g.semester,
            'course_id': g.course_id,
            'grade': g.grade
        } for g in grades
    ])

@app.route('/get_study_plans/<course_id>', methods=['GET'])
def get_study_plans(course_id):
    try:
        plans = StudyPlan.query.filter_by(id_course=course_id).all()
        data = []
        for p in plans:
            data.append({
                'id_plan': p.id_plan,
                'discipline': p.discipline,
                'semester': p.semester,
                'credit_of_discipline': p.credit_of_discipline,
                'exam_format': p.exam_format
            })
        return jsonify({'success': True, 'plans': data})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    
# Lab 8.5
# Добавляем новые API endpoints в app.py
@app.route('/add_attendance', methods=['POST'])
def add_attendance():
    try:
        data = request.get_json()
        new_attendance = StudentAttendance(
            student_id=data.get('student_id'),
            course_id=data.get('course_id'),
            attendance_date=datetime.strptime(data.get('attendance_date'), '%Y-%m-%d').date(),
            status=data.get('status')
        )
        db.session.add(new_attendance)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Attendance recorded'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/attendance/<int:student_id>', methods=['GET'])
def get_attendance(student_id):
    attendances = StudentAttendance.query.filter_by(student_id=student_id).all()
    return jsonify([{
        'id': a.id,
        'course_id': a.course_id,
        'attendance_date': a.attendance_date.isoformat(),
        'status': a.status
    } for a in attendances])

# @app.route("/about")
# def about():
#     return render_template("about.html")

# TẠO DATABASE NẾU CHƯA CÓ
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

import pytest
import json
import os
import sys

# Добавляем корневую директорию в путь Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import Student, Course, StudyPlan, StudentProgressLog

@pytest.fixture
def client():
    """Фикстура для создания тестового клиента и базы данных"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

@pytest.fixture
def init_database(client):
    """Фикстура для инициализации тестовых данных"""
    with app.app_context():
        # Очищаем базу данных
        db.drop_all()
        db.create_all()
        
        # Создаем тестовые данные
        student1 = Student(
            id_student=1,
            last_name="Иванов",
            full_name="Иван Иванович Иванов",
            year_of_admission=2023,
            form_of_study="Очная",
            education_level="Бакалавриат",
            course_code="CS101",
            group_number="ГРП-001",
            number_phone="+79991234567",
            email="ivanov@example.com"
        )
        
        student2 = Student(
            id_student=2,
            last_name="Петров",
            full_name="Петр Петрович Петров", 
            year_of_admission=2023,
            form_of_study="Заочная",
            education_level="Магистратура",
            course_code="MATH201",
            group_number="ГРП-002",
            number_phone="+79997654321",
            email="petrov@example.com"
        )
        
        course1 = Course(
            id_course="CS101",
            name_course="Программирование",
            total_hours=144,
            number_year="1",
            description="Основы программирования на Python"
        )
        
        course2 = Course(
            id_course="MATH201", 
            name_course="Математика",
            total_hours=120,
            number_year="2",
            description="Высшая математика"
        )
        
        study_plan = StudyPlan(
            id_plan="PLAN001",
            id_course="CS101",
            discipline="Программирование",
            semester=1,
            credit_of_discipline=4,
            exam_format="Экзамен"
        )
        
        # Добавляем в базу
        db.session.add(student1)
        db.session.add(student2)
        db.session.add(course1)
        db.session.add(course2)
        db.session.add(study_plan)
        db.session.commit()
        
        yield db
        
        # Очистка после тестов
        db.session.remove()
        db.drop_all()

# ЮНИТ-ТЕСТЫ

def test_student_model_creation():
    """Тестирование создания модели Student"""
    with app.app_context():
        student = Student(
            id_student=100,
            last_name="Сидоров",
            full_name="Сидор Сидорович Сидоров",
            year_of_admission=2024,
            form_of_study="Очная",
            education_level="Бакалавриат",
            course_code="CS101",
            group_number="ГРП-003",
            number_phone="+79998887766",
            email="sidorov@example.com"
        )
        
        assert student.id_student == 100
        assert student.last_name == "Сидоров"
        assert student.full_name == "Сидор Сидорович Сидоров"
        assert student.year_of_admission == 2024
        assert student.form_of_study == "Очная"

def test_course_model_creation():
    """Тестирование создания модели Course"""
    with app.app_context():
        course = Course(
            id_course="PHYS301",
            name_course="Физика",
            total_hours=180,
            number_year="3",
            description="Курс общей физики"
        )
        
        assert course.id_course == "PHYS301"
        assert course.name_course == "Физика"
        assert course.total_hours == 180
        assert course.number_year == "3"

def test_study_plan_model_creation():
    """Тестирование создания модели StudyPlan"""
    with app.app_context():
        plan = StudyPlan(
            id_plan="PLAN002",
            id_course="PHYS301",
            discipline="Физика",
            semester=2,
            credit_of_discipline=3,
            exam_format="Зачет"
        )
        
        assert plan.id_plan == "PLAN002"
        assert plan.discipline == "Физика"
        assert plan.semester == 2
        assert plan.credit_of_discipline == 3

# ИНТЕГРАЦИОННЫЕ ТЕСТЫ

def test_add_student_integration(client, init_database):
    """Интеграционный тест добавления студента"""
    student_data = {
        'id_student': 300,
        'last_name': 'Кузнецов',
        'full_name': 'Алексей Кузнецов',
        'year_of_admission': 2024,
        'form_of_study': 'Очная',
        'education_level': 'Бакалавриат',
        'course_code': 'CS101',
        'group_number': 'ГРП-004',
        'number_phone': '+79995554433',
        'email': 'kuznetsov@example.com'
    }
    
    response = client.post('/add_student', 
                         data=json.dumps(student_data),
                         content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['student']['last_name'] == 'Кузнецов'
    assert data['student']['email'] == 'kuznetsov@example.com'

def test_get_student_integration(client, init_database):
    """Интеграционный тест получения данных студента"""
    response = client.get('/student/1')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id_student'] == 1
    assert data['last_name'] == 'Иванов'
    assert data['full_name'] == 'Иван Иванович Иванов'

# def test_get_nonexistent_student(client, init_database):
#     """Тестирование получения несуществующего студента"""
#     response = client.get('/student/9999')
    
#     assert response.status_code == 404
#     data = json.loads(response.data)
#     assert 'error' in data

def test_add_course_integration(client, init_database):
    """Интеграционный тест добавления курса"""
    course_data = {
        'id_course': 'HIST401',
        'name_course': 'История',
        'total_hours': 90,
        'number_year': '1',
        'description': 'Курс истории России'
    }
    
    response = client.post('/add_course',
                         data=json.dumps(course_data),
                         content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['course']['name_course'] == 'История'

def test_get_course_integration(client, init_database):
    """Интеграционный тест получения данных курса"""
    response = client.get('/course/CS101')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id_course'] == 'CS101'
    assert data['name_course'] == 'Программирование'

def test_count_students_by_form(client, init_database):
    """Тестирование подсчета студентов по форме обучения"""
    response = client.get('/students/count/Очная')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['count'] == 1
    assert data['form_of_study'] == 'Очная'
    
    response = client.get('/students/count/Заочная')
    data = json.loads(response.data)
    assert data['count'] == 1

def test_get_students_by_group(client, init_database):
    """Тестирование получения студентов по группе"""
    response = client.get('/students/group/ГРП-001')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['group_number'] == 'ГРП-001'
    assert data[0]['full_name'] == 'Иван Иванович Иванов'

def test_get_course_info(client, init_database):
    """Тестирование получения информации об учебном плане"""
    response = client.get('/course/info/PLAN001')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id_plan'] == 'PLAN001'
    assert data['discipline'] == 'Программирование'
    assert data['semester'] == 1

def test_add_study_plan_integration(client, init_database):
    """Интеграционный тест добавления учебного плана"""
    plan_data = {
        'id_plan': 'PLAN003',
        'id_course': 'MATH201',
        'discipline': 'Высшая математика',
        'semester': 3,
        'credit_of_discipline': 5,
        'exam_format': 'Экзамен'
    }
    
    response = client.post('/add_studyplan',
                         data=json.dumps(plan_data),
                         content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['studyplan']['discipline'] == 'Высшая математика'

def test_add_grades_integration(client, init_database):
    """Интеграционный тест добавления оценок"""
    grade_data = {
        'id_log': 1,
        'semester': 1,
        'student_id': 1,
        'course_id': 'CS101',
        'grade': 'Отлично'
    }
    
    response = client.post('/add_grades',
                         data=json.dumps(grade_data),
                         content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['progress_log']['grade'] == 'Отлично'

def test_get_student_grades(client, init_database):
    """Тестирование получения оценок студента"""
    # Сначала добавляем оценку
    grade_data = {
        'id_log': 2,
        'semester': 1,
        'student_id': 2,
        'course_id': 'MATH201',
        'grade': 'Хорошо'
    }
    
    client.post('/add_grades',
               data=json.dumps(grade_data),
               content_type='application/json')
    
    # Затем получаем оценки
    response = client.get('/grades/student/2')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['grade'] == 'Хорошо'

# ТЕСТЫ ДЛЯ ОБРАБОТКИ ОШИБОК

def test_add_student_missing_data(client, init_database):
    """Тестирование добавления студента с отсутствующими обязательными полями"""
    invalid_data = {
        'id_student': 400,
        # Отсутствует last_name (обязательное поле)
        'full_name': 'Тест Тестович Тестов'
    }
    
    response = client.post('/add_student',
                         data=json.dumps(invalid_data),
                         content_type='application/json')
    
    # Ожидаем ошибку из-за отсутствия обязательных полей
    assert response.status_code == 500

def test_delete_student(client, init_database):
    """Тестирование удаления студента"""
    response = client.delete('/student/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data

def test_delete_nonexistent_student(client, init_database):
    """Тестирование удаления несуществующего студента"""
    response = client.delete('/student/9999')
    assert response.status_code == 404

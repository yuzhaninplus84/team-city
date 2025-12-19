-- Добавляем таблицу посещаемости
CREATE TABLE student_attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id VARCHAR(50) NOT NULL,
    attendance_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('present', 'absent', 'late')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES student (id_student),
    FOREIGN KEY (course_id) REFERENCES course (id_course)
);

-- Добавляем индекс для оптимизации запросов
CREATE INDEX idx_attendance_student_course ON student_attendance (
    student_id, course_id
);

-- Таблица для учета достижений студентов
CREATE TABLE IF NOT EXISTS student_achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    achievement_type VARCHAR(50) NOT NULL,
    achievement_name VARCHAR(200) NOT NULL,
    achievement_date DATE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES student(id_student)
);

-- Индекс для поиска достижений по студенту
CREATE INDEX IF NOT EXISTS idx_achievements_student 
ON student_achievements(student_id);

-- Индекс по типу достижения
CREATE INDEX IF NOT EXISTS idx_achievements_type 
ON student_achievements(achievement_type);
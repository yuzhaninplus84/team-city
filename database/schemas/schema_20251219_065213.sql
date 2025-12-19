-- Database Schema Export
-- Generated: 2025-12-19 06:52:13.227609
-- Database: student_portal.db

CREATE TABLE student (
	id_student INTEGER NOT NULL, 
	last_name VARCHAR(50) NOT NULL, 
	full_name VARCHAR(100) NOT NULL, 
	year_of_admission INTEGER NOT NULL, 
	form_of_study VARCHAR(20), 
	education_level VARCHAR(50), 
	course_code VARCHAR(20), 
	group_number VARCHAR(10), 
	number_phone VARCHAR(20), 
	email VARCHAR(120), 
	PRIMARY KEY (id_student), 
	UNIQUE (email)
);

CREATE TABLE course (
	id_course VARCHAR(50) NOT NULL, 
	name_course VARCHAR(100) NOT NULL, 
	total_hours INTEGER NOT NULL, 
	number_year VARCHAR(50) NOT NULL, 
	description TEXT, 
	PRIMARY KEY (id_course)
);

CREATE TABLE study_plan (
	id_plan VARCHAR(50) NOT NULL, 
	id_course VARCHAR(50), 
	discipline VARCHAR(100) NOT NULL, 
	semester INTEGER NOT NULL, 
	credit_of_discipline INTEGER NOT NULL, 
	exam_format VARCHAR(20) NOT NULL, 
	PRIMARY KEY (id_plan), 
	FOREIGN KEY(id_course) REFERENCES course (id_course)
);

CREATE TABLE student_progress_log (
	id_log INTEGER NOT NULL, 
	semester INTEGER, 
	student_id INTEGER, 
	course_id VARCHAR(50), 
	grade VARCHAR(20), 
	PRIMARY KEY (id_log), 
	FOREIGN KEY(student_id) REFERENCES student (id_student), 
	FOREIGN KEY(course_id) REFERENCES course (id_course)
);

-- Indexes

/*БД для работы телеграм бота ФЗФО*/

/*Уровень образования*/
CREATE TABLE Level_education (
	level_id SERIAL PRIMARY KEY,
	name_level varchar(20)
);

/*Специальности института на которых учатся студенты*/
CREATE TABLE Specialities(
	Speciality_id SERIAL PRIMARY KEY,
	Name_speciality VARCHAR(40),
	Code_speciality varchar(8),
	level_id INT,
	FOREIGN KEY (level_id) REFERENCES level_education(level_id) ON DELETE SET NULL
);

/*Формы обучения*/
CREATE TABLE Form_studies(
	Form_study_id SERIAL PRIMARY KEY,
	Name_form_study VARCHAR(20)
);

/*Группы студентов*/
CREATE TABLE Groups_student(
	Group_id SERIAL PRIMARY KEY,
	Name_group VARCHAR(10) NOT NULL UNIQUE,
	Start_studies DATE,
	Speciality_id INT NOT NULL,
	Form_study_id INT NOT NULL,
	FOREIGN KEY (Speciality_id) REFERENCES Specialities(Speciality_id) ON DELETE SET NULL,
	FOREIGN KEY (Form_study_id) REFERENCES Form_studies(Form_study_id) ON DELETE SET NULL
);

/*Информация о студентах*/
CREATE TABLE Students(
	Student_id SERIAL PRIMARY KEY,
	Surname VARCHAR(40) NOT NULL,
	First_name VARCHAR(40) NOT NULL,
	Second_name VARCHAR(40),
	Group_id INT,
	FOREIGN KEY (Group_id) REFERENCES Groups_student(Group_id)
);


/*Учетные данные для авторизации у телеграм-бота*/
CREATE TABLE Users_TGB(
	user_tgb_id SERIAL PRIMARY KEY,
	login_tgb varchar(40) unique NOT NULL,
	password_tgb varchar(40) NOT NULL,
	id_telegram varchar(40) UNIQUE,
	Student_id int UNIQUE,
	FOREIGN KEY (Student_id) REFERENCES Students(Student_id) ON DELETE SET NULL
);

/*Работодатели*/
CREATE TABLE Employers(
	Employer_id SERIAL PRIMARY KEY,
	Name_employer VARCHAR(100) UNIQUE NOT NULL
);

/*Таблица с трудоустройствами студентов*/
CREATE TABLE Employements (
	Employement_id SERIAL PRIMARY KEY,
	Student_id INT UNIQUE,
	Employer_id INT,
	FOREIGN KEY (Student_id) REFERENCES Students(Student_id) ON DELETE SET NULL,
	FOREIGN KEY (Employer_id) REFERENCES Employers(Employer_id) ON DELETE SET NULL
);

/*Типы сессий*/
CREATE TABLE Type_sessions(
	Type_session_id SERIAL PRIMARY KEY,
	Name_type_session VARCHAR(100) UNIQUE
);

/*Сессии*/
CREATE TABLE Sessions(
	Session_id SERIAL PRIMARY KEY,
	Start_session DATE,
	End_session DATE,
	Group_id INT,
	Type_session_id INT,
	FOREIGN KEY (Group_id) REFERENCES Groups_student(Group_id) ON DELETE SET NULL,
	FOREIGN KEY (Type_session_id) REFERENCES Type_sessions(Type_session_id) ON DELETE SET NULL
);

CREATE TABLE stored_documents(
    document_id SERIAL PRIMARY KEY,
    session_id int,
    student_id INT,
    date_document DATE,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (session_id) REFERENCES Sessions(session_id)
);
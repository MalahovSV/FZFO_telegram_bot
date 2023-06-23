CREATE OR REPLACE FUNCTION Add_ID_UserTG (login_user varchar, password_user varchar, telegram_id varchar)
  RETURNS BOOLEAN
  AS $BODY$
BEGIN
	IF (SELECT COUNT(*) from users_tgb WHERE login_tgb = $1 and password_tgb=$2)>0
		THEN
			UPDATE users_tgb
			SET id_telegram = $3
			WHERE login_tgb = $1;
			RETURN True;
		ELSE
			RETURN False;
	END IF;
END;
$BODY$
LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE add_document (var_session_id int, var_student_id int, var_date_document date)
AS $BODY$
BEGIN
	INSERT INTO stored_documents (session_id, student_id, date_document)
	VALUES($1, $2, $3);
END;
$BODY$
LANGUAGE plpgsql;






CREATE OR REPLACE FUNCTION get_document (var_date_doc date, var_telegram_id varchar)
RETURNS  SETOF public.stored_documents
AS $BODY$
BEGIN
	RETURN QUERY select document_id, sd.session_id, sd.student_id, sd.date_document from stored_documents sd
	JOIN students st ON st.student_id = sd.student_id
	JOIN users_tgb u ON u.student_id = st.student_id
	JOIN sessions s ON s.session_id = sd.session_id
	WHERE u.id_telegram = $2 and s.start_session > $1
	ORDER BY date_document ASC
	LIMIT 1;
END;
$BODY$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_All_data (var_telegram_id varchar, var_date_search date)
  RETURNS TABLE(
  					var_surname VARCHAR,
	  				var_first_name VARCHAR,
		  			var_second_name VARCHAR,
		  			var_name_group VARCHAR,
		  			var_code_speciality VARCHAR,
		  			var_name_speciality VARCHAR,
		  			var_start_session DATE,
		  			var_end_session DATE,
		  			var_name_type_session VARCHAR,
		  			var_name_form_study VARCHAR,
		  			var_name_level VARCHAR,
		  			var_name_employer VARCHAR
  )
  AS $BODY$
DECLARE
var_session_id int;
var_student_id int;

BEGIN
	IF NOT EXISTS (select * from get_document($2, $1))
	THEN
		BEGIN
			SELECT session_id INTO var_session_id
						   FROM students s
						   JOIN users_tgb u ON u.student_id = s.student_id
						   JOIN groups_student gs ON gs.group_id = s.group_id
						   JOIN specialities sp ON sp.speciality_id = gs.speciality_id
						   JOIN sessions sess ON sess.group_id = gs.group_id
						   WHERE id_telegram = $1 and start_session > $2
						   ORDER BY start_session
						   LIMIT 1;

			SELECT student_id INTO var_student_id FROM users_tgb WHERE id_telegram = $1;

			CALL add_document(var_session_id,
						  var_student_id,
						  $2);
		END;
	END IF;

	RETURN QUERY SELECT surname, first_name, second_name, name_group, code_speciality, name_speciality,
			start_session, end_session, name_type_session, name_form_study, name_level, name_employer
			FROM students s
			JOIN users_tgb u ON u.student_id = s.student_id
			JOIN groups_student gs ON gs.group_id = s.group_id
			JOIN specialities sp ON sp.speciality_id = gs.speciality_id
			JOIN sessions sess ON sess.group_id = gs.group_id
			JOIN type_sessions ts ON ts.type_session_id = sess.type_session_id
			JOIN form_studies fst ON fst.form_study_id = gs.form_study_id
			JOIN level_education le ON le.level_id = sp.level_id
			JOIN employements emp ON emp.student_id = s.student_id
			JOIN employers em ON em.employer_id = emp.employer_id
			WHERE id_telegram = $1 and start_session > $2
			ORDER BY start_session ASC;
END;
$BODY$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_data_for_document (var_telegram_id varchar, var_date_search date)
  RETURNS TABLE(
  					var_surname VARCHAR,
	  				var_first_name VARCHAR,
		  			var_second_name VARCHAR,
		  			var_document_id int,
		  			var_code_speciality VARCHAR,
		  			var_name_speciality VARCHAR,
		  			var_start_session DATE,
		  			var_end_session DATE,
		  			var_name_type_session VARCHAR,
		  			var_name_form_study VARCHAR,
		  			var_name_level VARCHAR,
		  			var_name_employer VARCHAR,
	  				var_name_group VARCHAR,
	  				var_date_document DATE
  )
  AS $BODY$
DECLARE
var_session_id int;
var_student_id int;

BEGIN
	IF NOT EXISTS (select * from get_document($2, $1))
	THEN
		BEGIN
			SELECT session_id INTO var_session_id
						   FROM students s
						   JOIN users_tgb u ON u.student_id = s.student_id
						   JOIN groups_student gs ON gs.group_id = s.group_id
						   JOIN specialities sp ON sp.speciality_id = gs.speciality_id
						   JOIN sessions sess ON sess.group_id = gs.group_id
						   WHERE id_telegram = $1 and start_session > $2
						   ORDER BY start_session
						   LIMIT 1;

			SELECT student_id INTO var_student_id FROM users_tgb WHERE id_telegram = $1;

			CALL add_document(var_session_id,
						  var_student_id,
						  $2);
		END;
	END IF;

	RETURN QUERY SELECT
						surname, 			--0 фамилия
						first_name, 		--1 имя
						second_name, 		--2 отчества
						document_id, 		--3 номер документа
						code_speciality, 	--4 код специальности
						name_speciality, 	--5 наименование специальности
						start_session, 		--6 начало сессии
						end_session, 		--7 конец сессии
						name_type_session, 	--8 тип сессии
						name_form_study, 	--9 форма обучения
						name_level, 		--10 уровень обучения
						name_employer,		--11 работодатель
						name_group,			--12 группа
						date_document       --13 дата документа
			FROM stored_documents sd
			JOIN students s ON s.student_id = sd.student_id
			JOIN users_tgb u ON u.student_id = s.student_id
			JOIN groups_student gs ON gs.group_id = s.group_id
			JOIN specialities sp ON sp.speciality_id = gs.speciality_id
			JOIN sessions sess ON sess.session_id = sd.session_id
			JOIN type_sessions ts ON ts.type_session_id = sess.type_session_id
			JOIN form_studies fst ON fst.form_study_id = gs.form_study_id
			JOIN level_education le ON le.level_id = sp.level_id
			JOIN employements emp ON emp.student_id = s.student_id
			JOIN employers em ON em.employer_id = emp.employer_id
			WHERE id_telegram = $1 and start_session > $2
			ORDER BY start_session ASC;
END;
$BODY$
LANGUAGE plpgsql;




CREATE TABLE absences (

id SERIAL PRIMARY KEY,

student_id INT,

session_id INT,

logged_at TIMESTAMP DEFAULT now()

);

CREATE OR REPLACE FUNCTION log_absence()

RETURNS TRIGGER AS $$

BEGIN

IF NEW.attended = FALSE THEN

INSERT INTO absences(student_id, session_id)

VALUES (NEW.student_id, NEW.session_id);

END IF;

RETURN NEW;

END;

$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_log_absence

AFTER INSERT ON attendance

FOR EACH ROW EXECUTE FUNCTION log_absence();
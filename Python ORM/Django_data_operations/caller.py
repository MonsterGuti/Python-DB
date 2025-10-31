import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Student


def add_students():
    Student.objects.create(
        student_id="FC5204",
        first_name="John",
        last_name="Doe",
        birth_date=date(1995, 5, 15),
        email="john.doe@university.com"
    )

    student_2 = Student(
        student_id="FE0054",
        first_name="Jane",
        last_name="Smith",
        birth_date=None,  # няма дата
        email="jane.smith@university.com"
    )
    student_2.save()

    student_3 = Student()
    student_3.student_id = "FH2014"
    student_3.first_name = "Alice"
    student_3.last_name = "Johnson"
    student_3.birth_date = date(1998, 2, 10)
    student_3.email = "alice.johnson@university.com"
    student_3.save()

    Student.objects.create(
        student_id="FH2015",
        first_name="Bob",
        last_name="Wilson",
        birth_date=date(1996, 11, 25),
        email="bob.wilson@university.com"
    )

def get_students_info():
    students = Student.objects.all()
    for student in students:
        print(f'Student №{student.student_id}: {student.first_name} {student.last_name}; Email: {student.email}')

def update_students_emails():
    students = Student.objects.all()
    for s in students:
        s.email = s.email.replace(s.email.split('@')[1], 'uni-students.com')
        s.save()

def truncate_students():
    students = Student.objects.all()
    students.delete()

if __name__ == "__main__":
    add_students()
    update_students_emails()
    get_students_info()
    truncate_students()
    get_students_info()

from main import db, Course, Student, Teacher, User, app

with app.app_context():
    student_username = "Jose Santos"
    teacher_username = "Susan Walker"
    student_name = "Jose Santos"
    teacher_name = "Susan Walker"

# Find the corresponding user IDs
student_user_id = User.query.filter_by(username=student_username).first().id
teacher_user_id = User.query.filter_by(username=teacher_username).first().id

# Update the foreign keys for students
students_to_update = Student.query.filter_by(name=student_username).all()
for student in students_to_update:
    student.user_id = student_user_id

# Update the foreign keys for teachers
teachers_to_update = Teacher.query.filter_by(name=teacher_username).all()
for teacher in teachers_to_update:
    teacher.user_id = teacher_user_id



"""
with app.app_context():
    new_login = User(username="Jose_Santy", type="student", password="12345")
    new_login2 = User(username="Susan Walker", type="teacher", password="Iamteacher")
    new_login3 = User(username="admin", type="admin", password="password")

    db.session.add(new_login)
    db.session.add(new_login2)
    db.session.add(new_login3)

    db.session.commit()
"""
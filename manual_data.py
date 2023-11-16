from main import db, Course, Student, Teacher, User, app

with app.app_context():
    student_username = "Nancy_L"
    teacher_username = "Ammon Hepworth"
    student_name = "Nancy Little"
    teacher_name = "Ammon Hepworth"

    # Find the corresponding user IDs
    student_user_id = User.query.filter_by(username=student_username).first().id
    teacher_user_id = User.query.filter_by(username=teacher_username).first().id


    #existing_student = Student.query.filter_by(name=student_name).all()
    exisiting_teacher = Teacher.query.filter_by(name=teacher_name).all()

    for t in exisiting_teacher:
        t.user_id = teacher_user_id
    db.session.commit()
    '''
    for s in existing_student:
     s.user_id = student_user_id
    db.session.commit()



with app.app_context():
    new_login = User(username="Ammon Hepworth", type="teacher", password="pass")

    db.session.add(new_login)

    db.session.commit()
'''
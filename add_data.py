from main import app, db, Login


with app.app_context():
    new_login = Login(name="student", type="student", password="12345")
    new_login2 = Login(name="teacher", type="teacher", password="Iamteacher")
    new_login3 = Login(name="admin", type="teacher", password="password")

    db.session.add(new_login)
    db.session.add(new_login2)
    db.session.add(new_login3)

    db.session.commit()

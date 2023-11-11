from flask import Flask, render_template,url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_data'
app.config['SECRET_KEY'] ='test'
csrf = CSRFProtect(app)
db = SQLAlchemy(app)

Login_manager = LoginManager()
Login_manager.init_app(app)
Login_manager.login_view = "login"





courses_students = db.Table(
    'courses_students',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True)
)    
courses_teachers = db.Table(
    'courses_teachers',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id'), primary_key=True)
)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    type = db.Column(db.String(7))
    password = db.Column(db.String(80), nullable=False)
    
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(80))
    teachers = db.relationship('Teacher', secondary=courses_teachers, back_populates='courses')
    students = db.relationship('Student', secondary=courses_students, back_populates='courses')
    course_name = db.Column(db.String(80))
    capacity = db.Column(db.Integer)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    courses = db.relationship('Course', secondary=courses_students,back_populates='students')
    grade = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    courses = db.relationship('Course', secondary=courses_teachers,back_populates='teachers')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Login_Form(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField("login")

@Login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def main():
    return render_template('main.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = Login_Form()
    if form.validate_on_submit():
        person = User.query.filter_by(username=form.username.data).first()
        if person:
            if person.password == form.password.data:
                login_user(person)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard',  methods=['GET','POST'])
@login_required
def dashboard():
    user = current_user
    if user.type == 'student':
        return render_template('student.html', user=current_user)
    elif user.type == 'teacher':
        return render_template('teacher.html', user=current_user)
    elif user.type == 'admin':
        return render_template('admin.html', user=current_user)
    else:
        return "Unknown type"

if __name__ == "__main__":
    app.run(debug=True)
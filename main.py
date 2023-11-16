from flask import Flask, render_template,url_for, redirect, jsonify, request
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
        min=2, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=2, max=20)], render_kw={"placeholder": "Password"})
    
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
                if (person.type == 'student'):
                    thePerson = Student.query.filter_by(user_id=person.id).first()
                    return redirect(url_for('dashboard',  user_name=thePerson.name))
                elif(person.type == 'teacher'):
                    thePerson = Teacher.query.filter_by(user_id=person.id).first()
                    return redirect(url_for('dashboard',  user_name=thePerson.name))
                else:
                    return redirect(url_for('dashboard', user_name ="admin"))
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
    user_name = request.args.get('user_name', None)
    if user.type == 'student':
        return render_template('student.html', user=current_user, user_name = user_name)
    elif user.type == 'teacher':
        return render_template('teacher.html', user=current_user,  user_name = user_name)
    elif user.type == 'admin':
        return render_template('admin.html', user=current_user,  user_name = user_name)
    else:
        return "Unknown type"
@app.route('/classes', methods = ['GET'])
@login_required
def student_class():
    user = current_user
    if user.type == 'student':
        student_list = Student.query.filter_by(user_id=user.id).all()
        print(student_list)
        if student_list:
            all_classes = []
            for s in student_list:
                classes = s.courses
                for c in classes:
                    teacher = c.teachers[0]
                    teacher_name = teacher.name
                    course_count = len(c.students)
                    class_info = {"id": c.id, "course_name": c.course_name, "time": c.time, "capacity": c.capacity, "amount":course_count, "teacher_name": teacher_name}
                    all_classes.append(class_info)
            return jsonify({"classes": all_classes})
        else:
            return jsonify({"message": "Student not found"}), 404
    elif user.type == 'teacher':
        teacher = Teacher.query.filter_by(user_id=user.id).first()
        if teacher:
            teacher_courses = teacher.courses
            teacher_classes = [
                {"name": teacher.name, "course_name": course.course_name, "time": course.time,"amount":len(course.students), "capacity": course.capacity, "id": course.id}
                for course in teacher_courses
            ]
            return jsonify({"classes": teacher_classes})
        else:
            return jsonify({"message": "Teacher not found"}), 404
    else:
        return jsonify({"message": "Access forbidden"}), 403
    
@app.route('/allclasses', methods = ['GET'])
@login_required
def all_classes():
    class_list = Course.query.all()
    all_classes = []
    for c in class_list:
         course_count = len(c.students)
         teacher = c.teachers[0]
         class_info = {"id": c.id, "course_name": c.course_name, "time": c.time, "capacity": c.capacity, "amount":course_count, "teacher_name": teacher.name}
         all_classes.append(class_info)
    return jsonify({"classes": all_classes})

@app.route('/enroll', methods=['POST','DELETE'])
@login_required
def enroll_in_class():
    print("working")
    user = current_user
    if user.type == 'student':
        data = request.get_json()
        students = Student.query.filter_by(user_id=user.id).all()
        if 'class_id' not in data:
            return jsonify({"message": "Class ID is required"}), 400
        class_id = data['class_id']
        course = Course.query.get(class_id)
        if not course:
            return jsonify({"message": "Class not found"}), 404
        for s in students:
            if s in course.students:
                course.students.remove(s)
                db.session.commit()
                return jsonify({"message": "Student removed from the class"}), 200
        if len(course.students) >= course.capacity:
            return jsonify({"message": "Class is full"}), 400
        course.students.append(students[0])
        db.session.commit()
        return jsonify({"message": "Enrollment successful"}), 200

    else:
        return jsonify({"message": "Access forbidden"}), 403

@app.route('/class/<int:ID>', methods=['GET'])
@login_required
def course_students(ID):
    user = current_user

    if user.type == 'teacher':
        teacher = Teacher.query.filter_by(user_id=user.id).first()
        course = Course.query.filter_by(id=ID).first()   
        if teacher and course in teacher.courses:
            enrollments = course.students  

            if enrollments:
                unique_student_ids = set()
                students_data = []

                for enrollment in enrollments:
                    student_id = enrollment.id  

                    if student_id not in unique_student_ids:
                        unique_student_ids.add(student_id)

                        student_data = {
                            "student_id": student_id,
                            "student_name": enrollment.name,
                            "grade": enrollment.grade
                        }
                        students_data.append(student_data)

                return jsonify({"students": students_data})
            else:
                return jsonify({"message": "No students found for the course"}), 404
        else:
            return jsonify({"message": "Access forbidden"}), 403
    else:
        return jsonify({"message": "Access forbidden"}), 403

@app.route('/class/<int:course_id>/update-grades', methods=['POST'])
@login_required
def update_grades(course_id):
    user = current_user

    if user.type == 'teacher':
        teacher = Teacher.query.filter_by(user_id=user.id).first()
        course = Course.query.get(course_id)

        if teacher and course in teacher.courses:
            data = request.get_json()

            if 'grades' not in data:
                return jsonify({"message": "Grades data is required"}), 400

            grade = data['grades']

            student_id = data['student_id']

            student = Student.query.filter_by(id = student_id).first()

            if student and student in course.students:
                student.grade = grade
                db.session.commit()
            else:
                    return jsonify({"message": f"Student with ID {student_id} not found or not enrolled in the course"}), 400

            return jsonify({"message": "Grades updated successfully"}), 200
        else:
            return jsonify({"message": "Access forbidden"}), 403
    else:
        return jsonify({"message": "Access forbidden"}), 403

@app.route('/admin', methods=['GET'])
def admin_dashboard():
    all_courses = Course.query.all()
    all_students = Student.query.all()
    all_teachers = Teacher.query.all()

    response_data = {
        "courses": [
            {"id": course.id, "course_name": course.course_name, "time": course.time, "capacity": course.capacity}
            for course in all_courses
        ],
        "students": [
            {"id": student.id, "name": student.name, "grade": student.grade}
            for student in all_students
        ],
        "teachers": [
            {"id": teacher.id, "name": teacher.name}
            for teacher in all_teachers
        ],
    }

    return jsonify(response_data)


if __name__ == "__main__":
    app.run(debug=True)

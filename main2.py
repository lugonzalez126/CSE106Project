from flask import Flask, request, render_template, redirect
from flask.helpers import url_for
from flask_admin import Admin
from flask_login import login_required, logout_user, login_user, current_user, LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///class-enrollment.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = "Walmart"

db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(userId):
    return Users.query.filter_by(userId = userId).first()

# Creating classes and tables to use for displaying and manipulating
# User table
class Users(UserMixin, db.Model):
    __tablename__ = "Users"
    userId = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    type = db.Column(db.Integer, nullable = False)
    # The type will give us a way to track the type of user we are dealing with, student,teacher, or Admin

    def __init__(self, username, name, password, type):
        self.username = username
        self.name = name
        self.password = password
        self.type = type

    def check_password(self, password):
        return self.password == password

    def get_id(self):
        return self.userId


# Courses
class Courses(db.Model):
    __tablename__ = "Courses"
    classId = db.Column(db.Integer, primary_key = True)
    className = db.Column(db.String, nullable = False)
    teacher = db.Column(db.String, nullable = False)
    time = db.Column(db.String, nullable = False)
    enrolled = db.Column(db.Integer, nullable = False)
    capacity = db.Column(db.Integer, nullable = False)

    def __init__(self, className, teacher, time, enrolled, capacity):
        self.className = className
        self.teacher = teacher
        self.time = time
        self.enrolled = enrolled
        self.capacity = capacity


# Used for Enrollment of classes
class Enrollment(db.Model):
    __tablename__ = "Enrollment"
    usersId = db.Column(db.ForeignKey("Users.userId"), primary_key = True)
    classesId = db.Column(db.ForeignKey("Courses.classId"), primary_key = True)
    grade = db.Column(db.Integer, nullable = False)

    def __init__(self, userId, classesId, grade):
        self.usersId = userId
        self.classesId = classesId
        self.grade = grade


# Login
@app.route("/", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        user = Users.query.filter_by(username=data['username']).first()
        if user is None or not user.check_password(data['password']):
            return (url_for('login'))[1:]
        login_user(user)
        if user.type == 0:
            return url_for('studentView')[1:]
        elif user.type == 1:
            return url_for('teacher_view')[1:]
        else:
            return url_for('admin')[1:]
    else:
        return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return url_for('login')[1:]


# ADMIN (has all capabilities, posting, editing, and deleting)
@app.route('/admin', methods = ["GET", "POST", "PUT", "DELETE"])
@login_required
def admin():
    # Adding new student to database
    if request.method == "GET":
        print("Get method")
        users = []
        courses = []
        grades = []
        #srows = Users.query.all()
        #crows = Courses.query.all()
        # Made a change to logic where instead of parsing through individual user rows and courses row, we instead
        # parse through enrollments, getting usersId and CoursesI from there. Because otherwise
        # we would also get admin and teacher Ids and inputs.
        erows = Enrollment.query.all()
        for row in erows:
            user = Users.query.filter_by(userId = row.usersId).first()
            users.append(user.name)
            course = Courses.query.filter_by(classId = row.classesId).first()
            courses.append(course.className)
            grades.append(row.grade)
        return render_template('adminview.html', users = Users.query.all(), courses = Courses.query.all(), length = (len(courses)), enrolledUsers = users, enrolledCourses = courses, enrolledGrades = grades)
    # Post functions
    elif request.method == "POST":
        print("Recieved Post")
        data = request.get_json()
        if data["post"] == "user":
            user = Users.query.filter_by(username=data["username"]).first()
            if user is None:
                user = Users(data["username"], data["name"], data["password"], int(data["type"]))
                db.session.add(user)
                db.session.commit()
                return "success"
        elif data["post"] == "class":
            course = Courses.query.filter_by(className=data["classname"]).first()
            if course is None:
                course = Courses(data["classname"], data["teacher"], data["time"], int(data["enrolled"]), int(data["capacity"]))
                db.session.add(course)
                db.session.commit()
                return "success"
        elif data["post"] == "enrollment":
            user = Users.query.filter_by(username = data["username"]).first()
            course = Courses.query.filter_by(className = data["classname"]).first()
            if user is not None and course is not None and user.type == 0:
                enroll = Enrollment(user.userId, course.classId, int(data["grade"]))
                course.enrolled = course.enrolled + 1
                db.session.add(enroll)
                db.session.commit()
                return "success"
    # Put functions
    elif request.method == "PUT":
        data = request.get_json()
        # If user is being updated
        if data["put"] == "user":
            user = Users.query.filter_by(username=data["original_name"]).first()
            if user is not None:
                if data["new_username"] != "":
                    user.username = data["new_username"]
                if data["new_name"] != "":
                    user.name = data["new_name"]
                if data["new_password"] != "":
                    user.password = data["new_password"]
                if data["new_acct"] != "":
                    user.type = int(data["new_acct"])
                db.session.commit()
                return "success"
        # If class is being updated
        if data["put"] == "class":
            print(data)
            course = Courses.query.filter_by(className=data["original_class"]).first()
            if course is not None:
                if data["new_class"] != "":
                    course.className = data["new_class"]
                if data["new_teacher"] != "":
                    course.teacher = data["new_teacher"]
                if data["new_time"] != "":
                    course.time = data["new_time"]
                if data["new_enrolled"] != "":
                    course.enrolled = int(data["new_enrolled"])
                if data["new_capacity"] != "":
                    course.capacity = int(data["new_capacity"])
                db.session.commit()
                return "success"
        elif data["put"] == "grade":
            user = Users.query.filter_by(username = data["name"]).first()
            course = Courses.query.filter_by(className = data["course"]).first()
            if user is not None and course is not None:
                enrolled_user = Enrollment.query.filter_by(usersId = user.userId, classesId = course.classId).first()
                enrolled_user.grade = data["grade"]
                db.session.commit()
                return "success"
    # Deleting function
    elif request.method == "DELETE":
        data = request.get_json()
        # Deleting a user
        if data["delete"] == "user":
            user = Users.query.filter_by(username=data["name"]).first()
            if user is not None:
                enroll = Enrollment.query.filter_by(usersId=user.userId)
                for row in enroll:
                    courses = Courses.query.filter_by(classId=row.classesId)
                    for course in courses:
                        course.enrolled = course.enrolled - 1
                    db.session.delete(row)
                db.session.delete(user)
                db.session.commit()
                return "success"
        # Deleting a class
        elif data["delete"] == "class":
            course = Courses.query.filter_by(className = data["class"]).first()
            if course is not None:
                enroll = Enrollment.query.filter_by(classesId = course.classId)
                for row in enroll:
                    db.session.delete(row)
                db.session.delete(course)
                db.session.commit()
                return "success"
        elif data["delete"] == "unenroll":
            user = Users.query.filter_by(username=data["name"]).first()
            course = Courses.query.filter_by(className=data["class"]).first()
            if user is not None and course is not None:
                enroll = Enrollment.query.filter_by(classesId=course.classId, usersId=user.userId).first()
                if enroll is not None:
                    course.enrolled = course.enrolled - 1
                    db.session.delete(enroll)
                    db.session.commit()
                    return "success"

# Student Views of Courses and editing to enroll into courses
# Student Views
@app.route("/student")
@login_required
def studentView():
    courses_list = []
    enrolled_classes = Enrollment.query.filter_by(usersId = current_user.userId)
    for course in enrolled_classes:
        courses_list.append(course.classesId)
    classes = Courses.query.filter(Courses.classId.in_(courses_list))
    return render_template('studentview.html', courses = classes, student = current_user.name)


# Student edit courses
@app.route("/student/courses", methods=["GET", "POST"])
@login_required
def studentEdit():
    # Editing their courses
    if request.method == "POST":
        data = request.get_json()
        course = Courses.query.filter_by(className=data["class_name"]).first()
        if course is not None and course.enrolled < course.capacity:
            enrollment = Enrollment(current_user.userId, course.classId, 0)
            db.session.add(enrollment)
            course.enrolled = course.enrolled+1
            db.session.commit()
            return "success"
        # Getting information
    if request.method == "GET":
        enrolled = Enrollment.query.filter_by(usersId = current_user.userId)
        enrolledClasses = []
        for course in enrolled:
            enrolledClasses.append(course.classesId)
        return render_template('studentEdit.html', courses = Courses.query.all(), enrollment = enrolledClasses)


# Teacher
# Teachers initial view of courses
@app.route("/teacher")
@login_required
def teacher_view():
    taught_classes = Courses.query.filter_by(teacher = current_user.name)
    return render_template('teacherview.html', courses = taught_classes, teacher = current_user.name)

# Teachers edits to classes and grades, based off of enrollment
@app.route("/teacher/<class_name>", methods=['GET', 'PUT'])
@login_required
def teacher_edit(class_name):
    # Acquiring grades, student ids, and course ids to be able to edit them and display them
    if request.method == "PUT":
        data = request.get_json()
        print(data)
        user = Users.query.filter_by(name = data["name"]).first()
        if user != None:
            course = Courses.query.filter_by(className = class_name).first()
            cId = course.classId
            enroll = Enrollment.query.filter_by(usersId = user.userId, classesId = cId).first()
            if enroll != None:
                enroll.grade = data["grade"]
                db.session.commit()

    listStudentIds = []
    listStudentNames = []

    grades = []
    # Courses
    course_details = Courses.query.filter_by(className = class_name).first()
    #Course ids
    classId = course_details.classId
    # Enrolled Students
    listEnrolled = Enrollment.query.filter_by(classesId = classId).order_by(Enrollment.usersId)
    for user in listEnrolled:
        grades.append(user.grade)
    # Acquire Student Ids
    for enrolled in listEnrolled:
        listStudentIds.append(enrolled.usersId)
    # Acquire Student users
    enrolled_users = Users.query.filter(Users.userId.in_(listStudentIds))
    # Acquire Student name
    for names in enrolled_users:
        listStudentNames.append(names.name)
    length = len(listStudentIds)

    return render_template('teacherview-details.html', name = class_name, students = listStudentNames, grades = grades, length = length)


if __name__ == '__main__':
    with app.app_context():
        #db.drop_all()
        db.create_all()
    app.run()
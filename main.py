from flask import Flask, render_template,url_for, redirect
from flask_sqlalchemy import SQLAlchemy
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


@Login_manager.user_loader
def load_user(user_id):
    return Login.query.get(int(user_id))

class Login(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    type = db.Column(db.String(7))
    password = db.Column(db.String(80), nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(80))
    teacher = db.Column(db.String(80))
    time = db.Column(db.String(80)) 
    enrolled = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
   

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    course_enrolled = db.Column(db.String(80))
    grade = db.Column(db.Integer)
    course_id = db.Column(db.Integer)




class Login_Form(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField("login")

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = Login_Form()
    if form.validate_on_submit():
        user = Login.query.filter_by(name=form.name.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user)
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
        return render_template('dashboard.html', user=current_user)

if __name__ == "__main__":
    app.run(debug=True)
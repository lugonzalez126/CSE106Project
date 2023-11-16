from main import db, Course, Student, Teacher, User, app
data = [
    {
        "class_name": "Math 101",
        "teacher_name": "Ralph Jenkins",
        "time": "MWF 10:00-10:50 AM",
        "capacity": 8,
        "students": [
            {"name": "Jose Santos", "grade": 92},
            {"name": "Betty Brown", "grade": 65},
            {"name": "John Stuart", "grade": 86},
            {"name": "Li Cheng", "grade": 77},
        ],
    },
    {
        "class_name": "Physics 121",
        "teacher_name": "Susan Walker",
        "time": "TR 11:00-11:50 AM",
        "capacity": 10,
        "students": [
            {"name": "Nancy Little", "grade": 53},
            {"name": "Li Cheng", "grade": 85},
            {"name": "Mindy Norris", "grade": 94},
            {"name": "John Stuart", "grade": 91},
            {"name": "Betty Brown", "grade": 88},
        ],
    },
    {
        "class_name": "CS 106",
        "teacher_name": "Ammon Hepworth",
        "time": "MWF 2:00-2:50 PM",
        "capacity": 10,
        "students": [
            {"name": "Aditya Ranganath", "grade": 93},
            {"name": "Yi Wen Chen", "grade": 85},
            {"name": "Nancy Little", "grade": 57},
            {"name": "Mindy Norris", "grade": 68},
        ],
    },
    {
        "class_name": "CS 162",
        "teacher_name": "Ammon Hepworth",
        "time": "TR 3:00-3:50 PM",
        "capacity": 4,
        "students": [
            {"name": "Aditya Ranganath", "grade": 99},
            {"name": "Nancy Little", "grade": 87},
            {"name": "Yi Wen Chen", "grade": 92},
            {"name": "John Stuart", "grade": 67},
        ],
    },
]


with app.app_context():
    for class_data in data:
      
        teacher = Teacher(name=class_data["teacher_name"])
        db.session.add(teacher)
        db.session.commit()

      
        course = Course(
            course_name=class_data["class_name"],
            time=class_data["time"],
            capacity=class_data["capacity"],
        )
        db.session.add(course)
        db.session.commit()

        for student_data in class_data["students"]:
            student = Student(name=student_data["name"], grade=student_data["grade"])
            course.students.append(student)

        course.teachers.append(teacher)
            
        db.session.commit()

print("Data added to the database.")
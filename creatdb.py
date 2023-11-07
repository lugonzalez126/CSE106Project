from main import app, db


#db.drop_all()

with app.app_context():
    db.create_all()
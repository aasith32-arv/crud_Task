from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root123@localhost/uki_school'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Student(db.Model):
    # __tablename__='students'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cgpa = db.Column(db.Float, nullable=False, default=0.0)
    is_active = db.Column(db.Boolean, default=True)
    join_date = db.Column(db.Date, nullable=False)
    create_at = db.Cloumn(db.DateTime, default=db.func.current_timestamp())

@app.route("/")
def home():
    return 'hello world'


if __name__ == '__main__':
    try:
       with app.app_context():
           db.session.execute(text('SELECT 1'))
           print("Database Connection Successful!")
           db.create_all()

    except Exception as e:
        print(f"Error connetion to database :{e}")



    app.run(debug=True)

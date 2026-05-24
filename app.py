from flask import Flask,request, jsonify

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import text

from datetime import datetime

app=Flask(__name__)

#MySQL Connection

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root123@localhost/uki_school'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Student Model

class Student(db.Model):

  __tablename__ = 'students'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)

  full_name = db.Column(db.String(100), nullable=False)

  email = db.Column(db.String(120), unique=True, nullable=False)

  age = db.Column(db.Integer, nullable=False)

  cgpa = db.Column(db.Float, nullable=False ,default=0.0)

  is_active = db.Column(db.Boolean, default=True)

  joined_date = db.Column(db.Date, nullable=False)

  created_at=db.Column(db.DateTime, default=datetime.utcnow())

  

@app.route('/')

def home():

    return 'Hello World!'

#Create new student

@app.route('/api/students', methods=['POST'])

def create_student():

            data = request.get_json()

            if not data:

                return jsonify({'error': 'No data provided'}), 400

            try:

                new_student = Student(

                full_name=data['full_name'],

                email=data['email'],

                age=data['age'],

                cgpa=data.get('cgpa', 0.0),

                is_active=data.get('is_active', True),

                joined_date=data['joined_date']

                )

                db.session.add(new_student)

                db.session.commit()

                return jsonify({'message': 'Student created successfully!'}), 201

    

            except Exception as e:

                db.session.rollback()

                return jsonify({'error': str(e)}), 400

#Get all students

@app.route('/api/students', methods=['GET'])

def get_students():

    students = Student.query.all()

    student_list = []

    for student in students:

        student_list.append({

            'id': student.id,

            'full_name': student.full_name,

            'email': student.email,

            'age': student.age,

            'cgpa': student.cgpa,

            'is_active': student.is_active,

            'joined_date': student.joined_date.strftime('%Y-%m-%d'),

            'created_at': student.created_at.strftime('%Y-%m-%d')

        })

    return jsonify(student_list)

#Get student by ID

@app.route('/api/students/<int:id>', methods=['GET'])

def get_student(id):

    

    student = Student.query.get(id)

    if not student:

        return jsonify({'error': 'Student not found'}), 404

    return jsonify({

        'id': student.id,

        'full_name': student.full_name,

        'email': student.email,

        'age': student.age,

        'cgpa': student.cgpa,

        'is_active': student.is_active,

        'joined_date': student.joined_date.strftime('%Y-%m-%d'),

        'created_at': student.created_at.strftime('%Y-%m-%d')

    })

#Update student by ID

@app.route('/api/students/<int:id>', methods=['PUT'])

def update_student(id):

    student = Student.query.get(id)

    if not student:

        return jsonify({'error': 'Student not found'}), 404

    data = request.get_json()

    if not data:

        return jsonify({'error': 'No data provided'}), 400

   

    try:

        student.full_name = data.get('full_name',student.full_name)

        student.email = data.get('email', student.email)

        student.age = data.get('age', student.age)

        student.cgpa = data.get('cgpa', student.cgpa)

        student.is_active = data.get('is_active', student.is_active)

        student.joined_date = data.get('joined_date', student.joined_date)

        db.session.commit()

        return jsonify({'message': 'Student updated successfully!'})

    except Exception as e:

        db.session.rollback()

        return jsonify({'error': str(e)}), 400

 

 

 

 

 

if __name__ == '__main__':

#Check Database Connection

    try:

        with app.app_context():

            db.session.execute(text('SELECT 1'))

            print("Database connection successful!")

            try:

                db.create_all()

                print("Tables created successfully!")

            except Exception as e:

                print(f"Error creating tables: {e}")

    except Exception as e:

        print(f"Error connecting to database: {e}")

    app.run(debug=True)






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

            try:

                data = request.get_json()

#Validate required fields:

                #Check if data is provided

                if not data:

                    return jsonify({'error': 'No data provided'}), 400

                #Validate full_name

                if not data.get('full_name'):

                    return jsonify({'error': 'Full name is required'}), 400

                #Validate email

                if not data.get('email'):

                    return jsonify({'error': 'Email is required'}), 400

                #Validate age

                if not data.get('age'):

                    return jsonify({'error': 'Age is required'}), 400

                if data.get('age') <= 0:

                    return jsonify({'error': 'Age must be a positive integer'}), 400

                #Validate joined_date

                if not data.get('joined_date'):

                    return jsonify({'error': 'Joined date is required'}), 400

                #Validate cgpa

                if not data.get('cgpa'):

                    return jsonify({'error': 'CGPA is required'}), 400

                #Check duplicate email

                existing_email = Student.query.filter_by(email=data['email']).first()

                if existing_email:  

                    return jsonify({'error': 'Email already exists'}), 400

              

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

    try:

        students = Student.query.all()

        if not students:

            return jsonify({'message': 'No students found'}), 404

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

        return jsonify(student_list),201

    except Exception as e:

        return jsonify({'error': str(e)}), 400

    

#Get student by ID

@app.route('/api/students/<int:id>', methods=['GET'])

def get_student(id):

    try:

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

    except Exception as e:

        return jsonify({'error': str(e)}), 400

#Update student by ID

@app.route('/api/students/<int:id>', methods=['PUT'])

def update_student(id):

    try:

        student = Student.query.get(id)

        data = request.get_json()

        if not data:

            return jsonify({'error': 'No data provided'}), 400

        if data.get('age') <= 0:

            return jsonify({'error': 'Age must be a positive integer'}), 400

        #Check duplicate email

        if data.get('email'):

            existing_email = Student.query.filter_by(email=data['email']).first()

            if existing_email and existing_email.id != id:

                return jsonify({'error': 'Email already exists'}), 400

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

#Delete student by ID

@app.route('/api/students/<int:id>', methods=['DELETE'])

def delete_student(id):

    try:

        student = Student.query.get(id)

        if not student:

           return jsonify({'error': 'Student not found'}), 404

  

        db.session.delete(student)

        db.session.commit()

        return jsonify({'message': f'Student ID {id} deleted successfully!'})

    except Exception as e:

        db.session.rollback()

        return jsonify({'error': str(e)}), 400
    




    #Course Model

class Course(db.Model):

  __tablename__ = 'courses'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)

  course_title = db.Column(db.String(100), nullable=False,unique=True)

  course_fee = db.Column(db.Float, nullable=False)

  duration_months = db.Column(db.Integer, nullable=False)

  description = db.Column(db.Text)

  is_available = db.Column(db.Boolean, default=True)

  created_at=db.Column(db.DateTime, default=datetime.utcnow())






  

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
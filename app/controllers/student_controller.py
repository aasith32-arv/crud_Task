
from flask import jsonify, request
from app import db
from app.models.student import Student
 
 
def create_student():
    try:
        data = request.get_json()
 
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        if not data.get('full_name'):
            return jsonify({'error': 'Full name is required'}), 400
        if not data.get('email'):
            return jsonify({'error': 'Email is required'}), 400
        if not data.get('age'):
            return jsonify({'error': 'Age is required'}), 400
        if data['age'] <= 0:
            return jsonify({'error': 'Age must be a positive integer'}), 400
        if not data.get('joined_date'):
            return jsonify({'error': 'Joined date is required'}), 400
        if not data.get('cgpa'):
            return jsonify({'error': 'CGPA is required'}), 400
 
        if Student.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
 
        student = Student(
            full_name=data['full_name'],
            email=data['email'],
            age=data['age'],
            cgpa=data.get('cgpa', 0.0),
            is_active=data.get('is_active', True),
            joined_date=data['joined_date'],
        )
        db.session.add(student)
        db.session.commit()
        return jsonify({'message': 'Student created successfully!'}), 201
 
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
 
 
def get_all_students():
    try:
        students = Student.query.all()
        if not students:
            return jsonify({'message': 'No students found'}), 404
        return jsonify([s.to_dict() for s in students]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
 
 
def get_student(id):
    try:
        student = Student.query.get(id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        return jsonify(student.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
 
 
def update_student(id):
    try:
        student = Student.query.get(id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
 
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
 
        if data.get('age') is not None and data['age'] <= 0:
            return jsonify({'error': 'Age must be a positive integer'}), 400
 
        if data.get('email'):
            existing = Student.query.filter_by(email=data['email']).first()
            if existing and existing.id != id:
                return jsonify({'error': 'Email already exists'}), 400
 
        student.full_name   = data.get('full_name', student.full_name)
        student.email       = data.get('email', student.email)
        student.age         = data.get('age', student.age)
        student.cgpa        = data.get('cgpa', student.cgpa)
        student.is_active   = data.get('is_active', student.is_active)
        student.joined_date = data.get('joined_date', student.joined_date)
 
        db.session.commit()
        return jsonify({'message': 'Student updated successfully!'}), 200
 
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
 
 
def delete_student(id):
    try:
        student = Student.query.get(id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
 
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': f'Student ID {id} deleted successfully!'}), 200
 
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
from flask import jsonify, request
from app import db
from app.models.course import Course
 
 
def create_course():
    try:
        data = request.get_json()
 
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        if not data.get('course_title'):
            return jsonify({'error': 'Course title is required'}), 400
        if not data.get('course_fee'):
            return jsonify({'error': 'Course fee is required'}), 400
        if data['course_fee'] <= 0:
            return jsonify({'error': 'Course fee must be a positive number'}), 400
        if not data.get('duration_months'):
            return jsonify({'error': 'Duration in months is required'}), 400
        if data['duration_months'] <= 0:
            return jsonify({'error': 'Duration in months must be a positive integer'}), 400
 
        if Course.query.filter_by(course_title=data['course_title']).first():
            return jsonify({'error': 'Course title already exists'}), 400
 
        course = Course(
            course_title=data['course_title'],
            course_fee=data['course_fee'],
            duration_months=data['duration_months'],
            description=data.get('description', ''),
        )
        db.session.add(course)
        db.session.commit()
        return jsonify({'message': 'Course created successfully!'}), 201
 
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
 
 
def get_all_courses():
    try:
        courses = Course.query.all()
        if not courses:
            return jsonify({'message': 'No courses found'}), 404
        return jsonify([c.to_dict() for c in courses]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
 
 
def get_course(id):
    try:
        course = Course.query.get(id)
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        return jsonify(course.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
 
 
def update_course(id):
    try:
        course = Course.query.get(id)
        if not course:
            return jsonify({'error': 'Course not found'}), 404
 
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
 
        if data.get('course_fee') is not None and data['course_fee'] <= 0:
            return jsonify({'error': 'Course fee must be a positive number'}), 400
 
        if data.get('course_title'):
            existing = Course.query.filter_by(course_title=data['course_title']).first()
            if existing and existing.id != id:
                return jsonify({'error': 'Course title already exists'}), 400
 
        course.course_title    = data.get('course_title', course.course_title)
        course.course_fee      = data.get('course_fee', course.course_fee)
        course.description     = data.get('description', course.description)
        course.duration_months = data.get('duration_months', course.duration_months)
        course.is_available    = data.get('is_available', course.is_available)
 
        db.session.commit()
        return jsonify({'message': 'Course updated successfully!'}), 200
 
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
 
 
def delete_course(id):
    try:
        course = Course.query.get(id)
        if not course:
            return jsonify({'error': 'Course not found'}), 404
 
        db.session.delete(course)
        db.session.commit()
        return jsonify({'message': f'Course ID {id} deleted successfully!'}), 200
 
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
from flask import Blueprint

from app.controllers.course_controller import (
    create_course,
    delete_course,
    get_all_courses,
    get_course,
    update_course,
)

course_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

course_bp.route('', methods=['POST'])(create_course)
course_bp.route('', methods=['GET'])(get_all_courses)
course_bp.route('/<int:id>', methods=['GET'])(get_course)
course_bp.route('/<int:id>', methods=['PUT'])(update_course)
course_bp.route('/<int:id>', methods=['DELETE'])(delete_course)

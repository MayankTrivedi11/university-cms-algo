# backend/src/controllers/course_controller.py
from flask import Blueprint, request, jsonify
from src.services.course_service import CourseService
from src.validators.course_validator import validate_course
from src.helper.algorand import get_algod_client

course_bp = Blueprint('course', __name__, url_prefix='/courses')

algod_client = get_algod_client() # Initialize Algorand client

course_service = CourseService(algod_client)


@course_bp.route('/', methods=['GET'])
def get_courses():
    courses = course_service.get_all_courses()
    return jsonify(courses)

@course_bp.route('/<course_id>', methods=['GET'])
def get_course(course_id):
     try:
        course = course_service.get_course_by_id(course_id)
        if course:
           return jsonify(course)
        else:
           return jsonify({"message": "Course not found"}), 404
     except Exception as e:
         return jsonify({"error": str(e)}), 500



@course_bp.route('/', methods=['POST'])
def create_course():
    data = request.get_json()

    # Validate the course data
    errors = validate_course(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        new_course = course_service.create_course(data)
        return jsonify(new_course), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@course_bp.route('/<course_id>', methods=['PUT'])
def update_course(course_id):
    data = request.get_json()

    errors = validate_course(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        updated_course = course_service.update_course(course_id, data)
        return jsonify(updated_course)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@course_bp.route('/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    try:
        course_service.delete_course(course_id)
        return jsonify({"message": "Course deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
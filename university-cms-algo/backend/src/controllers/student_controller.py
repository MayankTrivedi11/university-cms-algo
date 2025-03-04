# backend/src/controllers/student_controller.py
from flask import Blueprint, request, jsonify
from src.services.student_service import StudentService
from src.validators.student_validator import validate_student
from src.helper.algorand import get_algod_client

student_bp = Blueprint('student', __name__, url_prefix='/students')
algod_client = get_algod_client() # Initialize Algorand client

student_service = StudentService(algod_client)

@student_bp.route('/', methods=['GET'])
def get_students():
    students = student_service.get_all_students()
    return jsonify(students)

@student_bp.route('/<student_id>', methods=['GET'])
def get_student(student_id):
     try:
        student = student_service.get_student_by_id(student_id)
        if student:
           return jsonify(student)
        else:
           return jsonify({"message": "student not found"}), 404
     except Exception as e:
         return jsonify({"error": str(e)}), 500

@student_bp.route('/', methods=['POST'])
def create_student():
    data = request.get_json()

    # Validate the student data
    errors = validate_student(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        new_student = student_service.create_student(data)
        return jsonify(new_student), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@student_bp.route('/<student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()

    errors = validate_student(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        updated_student = student_service.update_student(student_id, data)
        return jsonify(updated_student)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@student_bp.route('/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        student_service.delete_student(student_id)
        return jsonify({"message": "student deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
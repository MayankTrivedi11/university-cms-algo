# backend/src/validators/student_validator.py

def validate_student(student_data):
    errors = {}

    if not student_data.get('student_id'):
        errors['student_id'] = 'Student ID is required.'
    if not student_data.get('name'):
        errors['name'] = 'Name is required.'
    if not student_data.get('major'):
        errors['major'] = 'Major is required.'
    if not student_data.get('email'):
        errors['email'] = 'Email is required.'
    if '@' not in student_data.get('email', ''):
        errors['email'] = 'Invalid email format.'

    return errors
    
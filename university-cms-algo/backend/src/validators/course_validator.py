# backend/src/validators/course_validator.py

def validate_course(course_data):
    errors = {}

    if not course_data.get('course_id'):
        errors['course_id'] = 'Course ID is required.'
    if not course_data.get('name'):
        errors['name'] = 'Name is required.'
    if not course_data.get('description'):
        errors['description'] = 'Description is required.'
    if not course_data.get('credits'):
        errors['credits'] = 'Credits is required.'
    try:
        credits = int(course_data.get('credits', 0))
        if credits <= 0:
            errors['credits'] = 'Credits must be a positive integer.'
    except ValueError:
        errors['credits'] = 'Credits must be an integer.'

    return errors
    
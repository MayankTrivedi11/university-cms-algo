# venv setup (optional, but highly recommended):
# python3 -m venv venv
# source venv/bin/activate  (Linux/macOS)
# venv\Scripts\activate  (Windows)
# pip install flask py-algorand-sdk python-dotenv

# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os

from src.controllers.course_controller import course_bp
from src.controllers.student_controller import student_bp


load_dotenv() # Load environment variables from .env file

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for frontend communication.

# Register blueprints
app.register_blueprint(course_bp)
app.register_blueprint(student_bp)

# Error handling
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
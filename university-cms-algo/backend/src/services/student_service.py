# backend/src/services/student_service.py

import json
from algosdk import account, mnemonic
from algosdk.future.transaction import SuggestedParams
from algosdk.encoding import decode_address
from src.helper.algorand import get_algod_client, create_app, call_app, delete_app, update_app
import os

class StudentService:
    def __init__(self, algod_client):
        self.algod_client = algod_client
        self.app_id = int(os.getenv("STUDENT_APP_ID", 0))
        self.private_key = os.getenv("PRIVATE_KEY")
        self.sender = account.address_from_private_key(self.private_key)

    def get_all_students(self):
        try:
            app_state = self.read_global_state()
            students = [value for key, value in app_state.items() if key.startswith('student_')]  # Fetch keys that starts with "student_"
            return students
        except Exception as e:
            raise Exception(f"Error getting all students: {e}")

    def get_student_by_id(self, student_id):
        try:
            app_state = self.read_global_state()
            student_key = f'student_{student_id}'
            student = app_state.get(student_key)
            if student:
                return student
            else:
                return None
        except Exception as e:
            raise Exception(f"Error getting student by ID: {e}")

    def create_student(self, student_data):
        try:
            app_args = [
                bytes("create_student", "utf-8"),
                bytes(student_data['student_id'], "utf-8"),
                bytes(student_data['name'], "utf-8"),
                bytes(student_data['major'], "utf-8"),
                bytes(student_data['email'], "utf-8")
            ]

            txn = call_app(
                self.algod_client,
                self.sender,
                self.private_key,
                self.app_id,
                app_args
            )

            return {"student_id": student_data['student_id'], "name": student_data['name'], "major": student_data['major'], "email": student_data['email']}
        except Exception as e:
            raise Exception(f"Error creating student: {e}")

    def update_student(self, student_id, student_data):
        try:
            app_args = [
                bytes("update_student", "utf-8"),
                bytes(student_id, "utf-8"),
                bytes(student_data['name'], "utf-8"),
                bytes(student_data['major'], "utf-8"),
                bytes(student_data['email'], "utf-8")
            ]

            txn = call_app(
                self.algod_client,
                self.sender,
                self.private_key,
                self.app_id,
                app_args
            )

            return {"student_id": student_id, "name": student_data['name'], "major": student_data['major'], "email": student_data['email']}
        except Exception as e:
            raise Exception(f"Error updating student: {e}")

    def delete_student(self, student_id):
        try:
            app_args = [
                bytes("delete_student", "utf-8"),
                bytes(student_id, "utf-8")
            ]

            txn = call_app(
                self.algod_client,
                self.sender,
                self.private_key,
                self.app_id,
                app_args
            )

            return {"message": "Student deleted successfully"}
        except Exception as e:
            raise Exception(f"Error deleting student: {e}")

    def read_global_state(self):
        try:
            app_info = self.algod_client.application_info(self.app_id)
            global_state = app_info['params']['global-state']
            readable_state = {}
            for state_var in global_state:
                key = state_var['key']
                value = state_var['value']
                key_str = bytes.fromhex(key).decode('utf-8')
                if value['type'] == 1:  # Byte array
                    readable_state[key_str] = bytes.fromhex(value['bytes']).decode('utf-8')
                else:  # Integer
                    readable_state[key_str] = value['uint']
            return readable_state
        except Exception as e:
            raise Exception(f"Error reading global state: {e}")
            
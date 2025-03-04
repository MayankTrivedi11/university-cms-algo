# backend/src/services/course_service.py

import os
from algosdk import algod
from algosdk import account, mnemonic
from algosdk.future import transaction
from algosdk.v2client import algod
from algosdk.future.transaction import TransactionParameters
from algosdk.encoding import decode_address

def read_teal_file(file_path):
    try:
        with open(file_path, 'r') as f:
            teal_code = f.read()
        return teal_code
    except Exception as e:
        raise Exception(f"Error reading TEAL file: {e}")

def compile_teal(client, teal_code):
    try:
        compile_response = client.compile(teal_code)
        return bytes.fromhex(compile_response['result'])
    except Exception as e:
        raise Exception(f"Error compiling TEAL code: {e}")


class CourseService:
    def __init__(self, algod_client):
        self.algod_client = algod_client
        self.app_id = int(os.getenv("COURSE_APP_ID", 0))  #  Retrieve from .env
        self.private_key = os.getenv("PRIVATE_KEY")
        self.sender = account.address_from_private_key(self.private_key)

        # Load approval and clear programs
        self.approval_program_path = "contracts/course_management_approval.teal.approval.bytecode"
        self.clear_program_path = "contracts/course_management_clear.teal.clear.bytecode"

        # Read and compile TEAL programs
        try:
            approval_teal_code = read_teal_file(self.approval_program_path)
            clear_teal_code = read_teal_file(self.clear_program_path)

            self.approval_program = compile_teal(self.algod_client, approval_teal_code)
            self.clear_program = compile_teal(self.algod_client, clear_teal_code)
        except Exception as e:
            raise Exception(f"Error loading or compiling TEAL programs: {e}")

    def deploy_smart_contract(self, global_schema, local_schema):
        try:
           app_id = create_app(self.algod_client, self.sender, self.private_key, self.approval_program, self.clear_program, global_schema, local_schema)
           return app_id
        except Exception as e:
            raise Exception(f"Error deploying smart contract: {e}")

    def create_course(self, course_data):
        try:
            # Get suggested parameters
            params = self.algod_client.suggested_params()
            # Get private key from mnemonic
            sk = os.getenv("PRIVATE_KEY")
            addr = account.address_from_private_key(sk)

            app_args = [
                bytes("create_course", "utf-8"),
                bytes(course_data['course_id'], "utf-8"),
                bytes(course_data['name'], "utf-8"),
                bytes(course_data['description'], "utf-8"),
                bytes(str(course_data['credits']), "utf-8")
            ]
            txn = transaction.ApplicationCallTxn(addr, params, int(os.getenv("COURSE_APP_ID", 0)), transaction.OnComplete.NoOpOC, app_args)
            # Sign the transaction
            signed_txn = txn.sign(sk)
            # Send the transaction
            txid = self.algod_client.send_transaction(signed_txn)
            # Wait for the transaction to be confirmed
            transaction_response = transaction.wait_for_confirmation(self.algod_client, txid, 4)
            # Get the application id
            app_id = transaction_response['application-index']

            return {"course_id": course_data['course_id'], "name": course_data['name'], "description": course_data['description'], "credits": course_data['credits']}
        except Exception as e:
            raise Exception(f"Error creating course: {e}")
            
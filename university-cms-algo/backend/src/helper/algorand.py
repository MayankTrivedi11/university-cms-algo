# backend/src/helper/algorand.py

import os
from algosdk import algod, mnemonic, account
from algosdk.future import transaction
from algosdk.v2client import algod
from algosdk.future.transaction import TransactionParameters
from algosdk.encoding import decode_address


def get_algod_client():
    algod_address = os.getenv("ALGOD_ADDRESS")
    algod_token = os.getenv("ALGOD_TOKEN")

    return algod.AlgodClient(algod_token, algod_address)

def create_app(client, sender, private_key, approval_program, clear_program, global_schema, local_schema):
    # Get suggested parameters
    params = client.suggested_params()
    # Create the transaction
    txn = transaction.ApplicationCreateTxn(
        sender,
        params,
        on_complete=transaction.OnComplete.NoOpOC.real,
        approval_program=approval_program,
        clear_program=clear_program,
        global_schema=global_schema,
        local_schema=local_schema,
    )

    # Sign the transaction
    signed_txn = txn.sign(private_key)
    # Send the transaction
    txid = client.send_transaction(signed_txn)
    # Wait for the transaction to be confirmed
    transaction_response = transaction.wait_for_confirmation(client, txid, 4)
    # Get the application id
    app_id = transaction_response['application-index']

    return app_id

def call_app(client, sender, private_key, app_id, app_args):
    # Get suggested parameters
    params = client.suggested_params()
    # Create the transaction
    txn = transaction.ApplicationCallTxn(
        sender,
        params,
        index=app_id,
        on_complete=transaction.OnComplete.NoOpOC.real,
        app_args=app_args
    )
    # Sign the transaction
    signed_txn = txn.sign(private_key)
    # Send the transaction
    txid = client.send_transaction(signed_txn)
    # Wait for the transaction to be confirmed
    transaction_response = transaction.wait_for_confirmation(client, txid, 4)

    return txid

def delete_app(client, sender, private_key, app_id):
    # Get suggested parameters
    params = client.suggested_params()
    # Create the transaction
    txn = transaction.ApplicationDeleteTxn(
        sender,
        params,
        index=app_id
    )
    # Sign the transaction
    signed_txn = txn.sign(private_key)
    # Send the transaction
    txid = client.send_transaction(signed_txn)
    # Wait for the transaction to be confirmed
    transaction_response = transaction.wait_for_confirmation(client, txid, 4)

    return txid

def update_app(client, sender, private_key, app_id, approval_program, clear_program):
    # Get suggested parameters
    params = client.suggested_params()
    # Create the transaction
    txn = transaction.ApplicationUpdateTxn(
        sender,
        params,
        index=app_id,
        approval_program=approval_program,
        clear_program=clear_program
    )
    # Sign the transaction
    signed_txn = txn.sign(private_key)
    # Send the transaction
    txid = client.send_transaction(signed_txn)
    # Wait for the transaction to be confirmed
    transaction_response = transaction.wait_for_confirmation(client, txid, 4)

    return txid
    
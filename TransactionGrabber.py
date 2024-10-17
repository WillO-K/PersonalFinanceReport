#!/usr/bin/env python3

import requests
import mysql.connector
import json
from datetime import datetime
from datetime import timedelta
import time

def get_bearer_token(token_file):
    try:
        with open(token_file, 'r') as file:
            token = file.read().strip()
        return token
    except FileNotFoundError:
        print("File not found")
        return None
token_file = 'yourDirectory/access_token.txt'

bearer_token = get_bearer_token(token_file)
print(bearer_token)

if not bearer_token:
    print("Bearer token not available. Investigate!") # This has yet to happen to me so good luck to anyone who encounters this
    exit(1)

# Details to connect to your database
db_connection = mysql.connector.connect(
    host="[insert host]",
    user="[insert user]",
    password="[insert password]",
    database= "[insert database]"
)

cursor = db_connection.cursor()

today = datetime.now()
yesterday = today - timedelta(days=1)
date_from = yesterday.strftime('%Y-%m-%d')
date_to = yesterday.strftime('%Y-%m-%d')

url = f'https://bankaccountdata.gocardless.com/api/v2/accounts/[account]/transactions/?date_from={date_from}&date_to={date_to}'


headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {bearer_token}',

}

json_data = {
    'secret_id': '[insert secret id]',
    'secret_key': '[insert secret key]',

}



response = requests.get(url, headers=headers)
print (time.strftime("%Y-%m-%d %H:%M"))

try:
    response_json = response.json()
    transactions = response_json.get("transactions", {}).get("booked", [])

    print(response_json)
    print(f"Found {len(transactions)} transactions.")

    if not transactions:
        print("No transactions found for the given date range.")
    
    insert_query = """
    INSERT IGNORE INTO lloyds_transactions (transactionId, entryReference, bookingDate, valueDate, amount, currency, creditorName, 
                              remittanceInformationUnstructured, proprietaryBankTransactionCode, internalTransactionId)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    rowCount = 0
    for transaction in transactions:
        rowCount = rowCount + 1
        transactionId = transaction.get("transactionId")
        entryReference = transaction.get("entryReference", None)  # Optional field, not all transactions seem to have one of these
        bookingDate = transaction.get("bookingDate")
        valueDate = transaction.get("valueDate")
        amount = transaction.get("transactionAmount", {}).get("amount")
        currency = transaction.get("transactionAmount", {}).get("currency")
        creditorName = transaction.get("creditorName") # Much to my own annoyance, not all transactions seem to have these either
        remittanceInformationUnstructured = transaction.get("remittanceInformationUnstructured", None)
        proprietaryBankTransactionCode = transaction.get("proprietaryBankTransactionCode", None)
        internalTransactionId = transaction.get("internalTransactionId", None)

        print(f"Inserting transaction: {transactionId}, {amount} {currency}, {creditorName}")
        
        cursor.execute(insert_query, (
            transactionId, entryReference, bookingDate, valueDate, amount, currency, creditorName, 
            remittanceInformationUnstructured, proprietaryBankTransactionCode, internalTransactionId
        ))

    db_connection.commit()

    print("Transactions found: ", rowCount) # TODO:Not actually too sure this is accurate either in terms of the count that is actually inserted into the db

except ValueError:
    print("Failed to parse JSON response.")
finally:
    cursor.close()
    db_connection.close()

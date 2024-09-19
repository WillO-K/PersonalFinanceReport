#!/usr/bin/env python3

import requests
import mysql.connector
import json
from datetime import datetime
from datetime import timedelta

def get_bearer_token(token_file):
    try:
        with open(token_file, 'r') as file:
            token = file.read().strip()
        return token
    except fileNotFound:
        print("File not found")
        return None
token_file = 'access_token.txt' #I know it's not very secure, but also I don't care. The database and Pi won't be public/exposed, and also this isn't a professional project.

bearer_token = get_bearer_token(token_file)

if not bearer_token:
    print("Bearer token not available. Don't know why, investigate!")
    exit(1)

db_connection = mysql.connector.connect(
    host="GetYourOwn!",
    user="GetYourOwn!",
    password="GetYourOwn!",
    database="GetYourOwn!"
)

cursor = db_connection.cursor()

today = datetime.now()
yesterday = today - timedelta(days=1) 
date_from = yesterday.strftime('%Y-%m-%d')
date_to = yesterday.strftime('%Y-%m-%d')

url = f'https://bankaccountdata.gocardless.com/api/v2/accounts/GetYourOwnAccountKey/transactions/?date_from={date_from}&date_to={date_to}'

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {bearer_token}',

}

json_data = {
    'secret_id': 'GetYourOwn!',
    'secret_key': 'GetYourOwn!',

}

response = requests.get(url, headers=headers)
#I'm printing all of this because it gets output to a log file during the cron job. If something goes wrong, I can just look at the log and troubleshoot from there. 
try:
  #toDo: Add json.dumps here so the output is less of an eyesore and formatted. Not really important right now though. 
    response_json = response.json()
    transactions = response_json.get("transactions", {}).get("booked", [])

    print(response_json)
    print(f"Found {len(transactions)} transactions.")

    if not transactions:
        print("No transactions found for date range.")
  
    insert_query = """
    INSERT IGNORE INTO lloyds_transactions (transactionId, entryReference, bookingDate, valueDate, amount, currency, creditorName, 
                              remittanceInformationUnstructured, proprietaryBankTransactionCode, internalTransactionId)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for transaction in transactions:
        transactionId = transaction.get("transactionId")
        entryReference = transaction.get("entryReference", None) 
        bookingDate = transaction.get("bookingDate")
        valueDate = transaction.get("valueDate")
        amount = transaction.get("transactionAmount", {}).get("amount")
        currency = transaction.get("transactionAmount", {}).get("currency")
        creditorName = transaction.get("creditorName")
        remittanceInformationUnstructured = transaction.get("remittanceInformationUnstructured", None)
        proprietaryBankTransactionCode = transaction.get("proprietaryBankTransactionCode", None)
        internalTransactionId = transaction.get("internalTransactionId", None)

        print(f"Inserting transaction: {transactionId}, {amount} {currency}, {creditorName}")
        
        cursor.execute(insert_query, (
            transactionId, entryReference, bookingDate, valueDate, amount, currency, creditorName, 
            remittanceInformationUnstructured, proprietaryBankTransactionCode, internalTransactionId
        ))

    db_connection.commit()

    print(f"Inserted {cursor.rowcount} transactions into the database.")  # toDo: Fix this... this kind of doesn't work as I expected it to right now, I don't think, but it's not significant.

except ValueError:
    print("Failed to parse JSON response.")
finally:
    cursor.close()
    db_connection.close()

import requests
import json


def invalid():
    print("Invalid choice")

def printResponse(response):
    try:
        response_json = response.json()
        print("Response JSON")
        print(json.dumps(response_json, indent=4))
    except ValueError:
        print("Response Text:", response.text)

def Step1():
    secret_id = input("Input your secret ID")
    secret_key = input("Input your secret key")
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    json_data = {
        'secret_id': secret_id,
        'secret_key': secret_key,
    }
    response = requests.post('https://bankaccountdata.gocardless.com/api/v2/token/new/', headers=headers, json=json_data)
    print (printResponse(response))

def Step2(): 
    bearer = input("Input your bearer token")
    headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer '+ bearer,
    }

    params = {
    'country': 'gb',
    }

    response = requests.get('https://bankaccountdata.gocardless.com/api/v2/institutions/', params=params, headers=headers)
    print (printResponse(response))

def Step3():
    institution_id = input("Institution ID: ")
    bearer = input("Input your bearer token")
    headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+ bearer,
    }

    json_data = {
    'institution_id': institution_id,
    'max_historical_days': '30',
    'access_scope': [
        'balances',
        'details',
        'transactions',
    ],
    }

    response = requests.post('https://bankaccountdata.gocardless.com/api/v2/agreements/enduser/', headers=headers, json=json_data)
    print (printResponse(response))

def Step4():
    institution_id = input("Institution ID: ")
    bearer = input("Input your bearer token")
    ref = input("Input a reference (can be anything)")
    agreement_id = input("Input your agreement uid")
    headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+ bearer,
    }

    json_data = {
    'redirect': 'http://www.kembledatasolutions.co.uk',
    'institution_id': institution_id,
    'reference': ref,
    'agreement': agreement_id,
    'user_language': 'EN',
    }

    response = requests.post('https://bankaccountdata.gocardless.com/api/v2/requisitions/', headers=headers, json=json_data)
    print (printResponse(response))

def Step5():
    bearer = input("Input your bearer token: ")
    req_id = input("Input the requisition ID: ")

    headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer '+ bearer,
    }

    response = requests.get('https://bankaccountdata.gocardless.com/api/v2/requisitions/'+req_id+'/', headers=headers,)
    print (printResponse(response))

def Step6():
    bearer = input("Input your bearer token: ")
    account_id = input("Input your account id: ")
    headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer '+ bearer,
    }

    response = requests.get('https://bankaccountdata.gocardless.com/api/v2/accounts/'+account_id+'/',headers=headers,)
    print (printResponse(response))


print("Before coming here, go generate your secrets at GoCardless!")
print("---MENU---")
print("1. Get Access Token")
print("2. Choose a Bank")
print("3. Create an End User Agreement")
print("4. Build a Link")
print("5. List Accounts")
print("6. Account Details/balances/transactions")

option = input("Pick an option /n")

while True:
    if option == '1':
        Step1()
    elif option =='2':
        Step2() 
    elif option =='3':
        Step3() 
    elif option =='4':
        Step4() 
    elif option =='5':
        Step5() 
    elif option =='6':
        Step6() 
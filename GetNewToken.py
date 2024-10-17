#!/usr/bin/env python3

import requests
import json
import sys
import time
import os

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

json_data = {
    'refresh': '[Insert your refresh token here]',
}

response = requests.post('https://bankaccountdata.gocardless.com/api/v2/token/refresh/', headers=headers, json=json_data)

print(f"Current directory: {os.getcwd()}")  # Wasn't convinced that this was saving the token to where I wanted it to be, so used this as debugging, and cba to take it out

try:
    print (time.strftime("%Y-%m-%d %H:%M"))
    response_json = response.json()
    print("Response JSON")
    print(json.dumps(response_json, indent=4))
    access_token = response_json['access']
    print(access_token)
    token_file = "yourDirectory/access_token.txt"

    with open(token_file, 'w') as file:
        file.write(access_token)
        file.close()

except ValueError:
    print("Response Text:", response.text)
    

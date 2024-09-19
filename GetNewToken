#!/usr/bin/env python3

import requests
import json
import sys

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

json_data = {
    'refresh': 'GetYourOwnRefreshToken!',
}

response = requests.post('https://bankaccountdata.gocardless.com/api/v2/token/refresh/', headers=headers, json=json_data)

try:
    response_json = response.json()
    print("Response JSON")
    print(json.dumps(response_json, indent=4))
    access_token = response_json['access']
    print(access_token)
    token_file = "access_token.txt"
    #Yeah I mean, not the most secure way to handle tokens, but it's just a fun personal project and the Pi is secure. 
    #'w' because we don't want tokens to get appended, we want them to overwrite what's already there. Otherwise my other script is going to go bonkers when it finds more than 1 token knocking around.
    with open(token_file, 'w') as file:
        file.write(access_token)

except ValueError:
    print("Response Text:", response.text)
    

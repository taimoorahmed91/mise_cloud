import urllib3
import requests
import sys
import json
import mysql.connector
import contextlib
import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

fqdn = sys.argv[1]

url1 = "https://"
url2 = "/ers/config/op/systemconfig/iseversion"
url = url1 + fqdn + url2

payload = {}

with open('credentials.txt') as file:
    # Execute the code in a separate namespace
    namespace = {}
    exec(file.read(), namespace)
    
    # Extract the 'headers' variable
    headers = namespace.get('headers', {})

# Send the request
response = requests.request("GET", url, headers=headers, data=payload, verify=False)

# Print the response code (commented out)
# print("Response Code:", response.status_code)

# Skip JSON response processing if response code is 401
if response.status_code == 401:
    print("Unauthorized.")  # Commented out
    pass
else:
    # Process the JSON response
    json_response = response.json()
    resources = json_response['OperationResult']['resultValue'][0]['name']
    print(resources)  # Commented out

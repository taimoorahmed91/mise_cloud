import urllib3
import requests
import sys
import json
import mysql.connector
import contextlib
import datetime
import ast

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

fqdn = sys.argv[1]

url1 = "https://"
url2 = "/api/v1/deployment/node"
url = url1 + fqdn + url2

payload = {}
with open('credentials.txt') as file:
    # Execute the code in a separate namespace
    namespace = {}
    exec(file.read(), namespace)
    
    # Extract the 'headers' variable
    headers = namespace.get('headers', {})

response = requests.request("GET", url, headers=headers, data=payload, verify=False)

# Parse the JSON response
json_response = response.json()
resources = json_response['response']

insert_query = "INSERT INTO nodes (fqdn, node, ipaddress, roles, services, nodestatus) VALUES (%s, %s, %s, %s, %s, %s)"
insert_values = []

for resource in resources:
    node = resource['fqdn']
    ipaddress = resource['ipAddress']
    roles = ', '.join(resource['roles']) if resource['roles'] else '-'  # Convert roles to a comma-separated string, or use hyphen if empty
    services = ', '.join(resource['services']) if resource['services'] else '-'  # Convert services to a comma-separated string, or use hyphen if empty
    nodestatus = resource['nodeStatus']
    print(node)
    print(services)
    insert_values.append((fqdn, node, ipaddress, roles, services, nodestatus))

# Establish a database connection
connection = mysql.connector.connect(
    host='127.0.0.1',
    database='mise',
    user='root',
    password='C1sc0123@'
)
cursor = connection.cursor(dictionary=True)

# Use executemany to insert multiple rows at once
cursor.executemany(insert_query, insert_values)

# Commit the changes and close the cursor and connection
connection.commit()
cursor.close()
connection.close()

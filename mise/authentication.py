import os
import urllib3
import requests
import sys
import json
import mysql.connector
import contextlib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

isename = sys.argv[1]
policysetid = sys.argv[2]
policysetname = sys.argv[3]

connection = mysql.connector.connect(
    host='database',
    database='mise',
    user='root',
    password='C1sc0123@'
)
cursor = connection.cursor(dictionary=True)

authentication = "/authentication"

firsthalfurl = "https://"
secondhalfurl = "/api/v1/policy/network-access/policy-set/"
url = firsthalfurl + isename + secondhalfurl + policysetid + authentication

payload = {}

with open('/var/www/html/mise/v0.1/credentials.txt') as file:
    namespace = {}
    exec(file.read(), namespace)
    headers = namespace.get('headers', {})

response = requests.get(url, headers=headers, data=payload, verify=False)
result = response.text

json_response = response.json()
resources = json_response['response']

length = len(resources)

initial_filename = "/root/ise-landscape/mise/configs/authentications/"
initial_webfilename = "/var/www/html/mise/v0.1/configs/authentications/"

# Ensure the directories exist
os.makedirs(os.path.dirname(initial_filename), exist_ok=True)
os.makedirs(os.path.dirname(initial_webfilename), exist_ok=True)

# Prepare the batch insert statement
insert_query = "INSERT INTO authentication (authentication, authenticationid, policyset, isename, get_code, href) VALUES (%s, %s, %s, %s, %s, %s)"
insert_values = []

for resource in resources:
    my_id = resource['rule']['id']
    my_name = resource['rule']['name']
    srcauthurl = url + "/" + my_id
    href = resource['link']['href']
    response2 = requests.get(srcauthurl, headers=headers, data=payload, verify=False)
    text_result = response2.text
    json_response2 = response2.json()
    initial_result = json_response2['response']
    #del initial_result['rule']['rank']
    del initial_result['rule']['id']
    final_result = json.dumps(initial_result, indent=4)
    filename = initial_filename + my_id
    filename_web = initial_webfilename + my_id
    with open(filename, "w") as o:
        with contextlib.redirect_stdout(o):
            print(final_result)
    with open(filename_web, "w") as o:
        with contextlib.redirect_stdout(o):
            print(final_result)
    response_post = str(response2)[1:-1]
    insert_values.append((my_name, my_id, policysetname, isename, response_post, href))

# Execute the batch insert
cursor.executemany(insert_query, insert_values)
connection.commit()

# Delete query
delete_query = """
    DELETE t1 FROM authentication t1
    INNER JOIN authentication t2 ON CONCAT(t1.authenticationid, t1.isename) = CONCAT(t2.authenticationid, t2.isename)
    WHERE t1.id < t2.id
"""

# Execute delete query
cursor.execute(delete_query)
connection.commit()

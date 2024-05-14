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
    host='127.0.0.1',
    database='mise',
    user='root',
    password='C1sc0123@'
)

authorization = "/authorization"
firsthalfurl = "https://"
secondhalfurl = "/api/v1/policy/network-access/policy-set/"

url = firsthalfurl + isename + secondhalfurl + policysetid + authorization

payload = {}
#headers = {
#    'Content-Type': 'application/json',
#    'Accept': 'application/json',
#    'Authorization': 'Basic YWRtaW46QzFzYzAxMjNA',
#}


with open('credentials.txt') as file:
    # Execute the code in a separate namespace
    namespace = {}
    exec(file.read(), namespace)
    
    # Extract the 'headers' variable
    headers = namespace.get('headers', {})


response = requests.get(url, headers=headers, data=payload, verify=False)
result = response.text

json_response = response.json()
length = len(json_response['response'])

initial_filename = "/root/ise-landscape/mise/configs/authorizations/"
initial_webfilename = "/var/www/html/mise/v0.1/configs/authorizations/"

insert_query = "INSERT INTO authorization (authorization, authorizationid, policyset, isename, get_code,href) VALUES (%s, %s, %s, %s, %s,%s)"
insert_values = []

for i in range(length):
    my_id = json_response['response'][i]['rule']['id']
    my_name = json_response['response'][i]['rule']['name']
    srcauthurl = url + "/" + my_id
    href = json_response['response'][i]['link']['href']
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
    response_post = str(response2)
    response_post = response_post[:-1]
    response_post = response_post[1:]
    insert_values.append((my_name, my_id, policysetname, isename, response_post,href))

cursor = connection.cursor(dictionary=True)
cursor.executemany(insert_query, insert_values)
connection.commit()

# Delete query
delete_query = """
    DELETE t1 FROM authorization t1
    INNER JOIN authorization t2 ON CONCAT(t1.authorizationid, t1.isename) = CONCAT(t2.authorizationid, t2.isename)
    WHERE t1.id < t2.id
"""

# Execute delete query
cursor.execute(delete_query)
connection.commit()
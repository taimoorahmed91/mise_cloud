import urllib3
import requests
import sys
import json
import mysql.connector
import contextlib
import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

fqdn = sys.argv[1]
inheritid = sys.argv[2]

connection = mysql.connector.connect(
    host='127.0.0.1',
    database='mise',
    user='root',
    password='C1sc0123@'
)
cursor = connection.cursor(dictionary=True)

url1 = "https://"
url2 = "/api/v1/policy/network-access/policy-set"
url = url1 + fqdn + url2

initial_filename = "/root/ise-landscape/mise/configs/policyset/"
initial_webfilename = "/var/www/html/mise/v0.1/configs/policyset/"

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


### set time parameters
current_time = datetime.datetime.now()

# Format the time as a string
time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")




file_path = "/var/www/html/mise/v0.1/logging/policyset-logs"
with open(file_path, "a") as file:
    # Append the output to the file
    file.write(time_string + "\n")
    file.write(result)


json_response = response.json()
policy_sets = json_response['response']

# Prepare the batch insert statement
insert_query = "INSERT INTO policyset (policyset, policysetid, isename, get_code, href, inheritid) VALUES (%s, %s, %s, %s, %s, %s)"
insert_values = []

for policy_set in policy_sets:
    my_id = policy_set['id']
    my_name = policy_set['name']
    srcauthurl = url + "/" + my_id
    href = policy_set['link']['href']
    response2 = requests.get(srcauthurl, headers=headers, data=payload, verify=False)
    text_result = response2.text
    json_response2 = response2.json()
    initial_result = json_response2['response']
    #del initial_result['rank']
    del initial_result['id']
    final_result = json.dumps(initial_result, indent=4)
    filename = initial_filename + my_id
    filename_web = initial_webfilename + my_id
    with open(filename_web, "w") as o:
        with contextlib.redirect_stdout(o):
            print(final_result)
    with open(filename, "w") as o:
        with contextlib.redirect_stdout(o):
            print(final_result)
    
    response_post = str(response2)[1:-1]
    #print(inheritid)
    insert_values.append((my_name, my_id, fqdn, response_post, href, inheritid))

# Execute the batch insert
cursor.executemany(insert_query, insert_values)
connection.commit()

# Delete query
delete_query = """
    DELETE t1 FROM policyset t1
    INNER JOIN policyset t2 ON CONCAT(t1.policysetid, t1.isename) = CONCAT(t2.policysetid, t2.isename)
    WHERE t1.id  < t2.id
"""

# Execute delete query
cursor.execute(delete_query)
connection.commit()
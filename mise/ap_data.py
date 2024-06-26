import os
import urllib3
import requests
import sys
import json
import mysql.connector
import contextlib
import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

fqdn = sys.argv[1]

connection = mysql.connector.connect(
    host='database',
    database='mise',
    user='root',
    password='C1sc0123@'
)
cursor = connection.cursor(dictionary=True)

url1 = "https://"
url2 = "/ers/config/allowedprotocols"
url = url1 + fqdn + url2

initial_webfilename = "/var/www/html/mise/v0.1/configs/ap/"

# Ensure the directories exist
os.makedirs(os.path.dirname(initial_webfilename), exist_ok=True)


payload = {}
#headers = {
#    'Content-Type': 'application/json',
#    'Accept': 'application/json',
#    'Authorization': 'Basic YWRtaW46QzFzYzAxMjNA',
#}

with open('/var/www/html/mise/v0.1/credentials.txt') as file:
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




file_path = "/var/www/html/mise/v0.1/logging/ap-logs"
os.makedirs(os.path.dirname(file_path), exist_ok=True)
with open(file_path, "a") as file:
    # Append the output to the file
    file.write(time_string + "\n")
    file.write(result)





json_response = response.json()
resources = json_response['SearchResult']['resources']

# Prepare the batch insert statement
insert_query = "INSERT INTO ap (ap, apid, isename, get_code, href) VALUES (%s, %s, %s, %s, %s)"
insert_values = []

for resource in resources:
    try:
        my_id = resource['id']
        my_name = resource['name']
        srcauthurl = url + "/" + my_id
        href = resource['link']['href']
        #print(href)
        response2 = requests.get(srcauthurl, headers=headers, data=payload, verify=False)
        text_result = response2.text
        filename_web = initial_webfilename + my_id
        with open(filename_web, "w") as o:
            with contextlib.redirect_stdout(o):
                print(text_result)

        response_post = str(response2)
        response_post = response_post[:-1]
        response_post = response_post[1:]
        insert_values.append((my_name, my_id, fqdn, response_post, href))

    except IndexError:
        break

# Batch insert the data
cursor.executemany(insert_query, insert_values)
connection.commit()

# Delete query
delete_query = """
    DELETE t1 FROM ap t1
    INNER JOIN ap t2 ON CONCAT(t1.apid, t1.isename) = CONCAT(t2.apid, t2.isename)
    WHERE t1.id < t2.id
"""


# Execute delete query
cursor.execute(delete_query)
connection.commit()


import urllib3
import requests
import sys
import json
import mysql.connector
import contextlib
import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# MySQL credentials
connection = mysql.connector.connect(
    host='127.0.0.1',
    database='mise',
    user='root',
    password='C1sc0123@'
)
cursor = connection.cursor(dictionary=True)


### set time parameters
current_time = datetime.datetime.now()

# Format the time as a string
time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")


fqdn = sys.argv[1]

url1 = "https://"
url2 = "/ers/config/downloadableacl"

url = url1 + fqdn + url2

initial_webfilename = "/var/www/html/mise/v0.1/configs/dacl/"

payload={}
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
resources = json_response['SearchResult']['resources']


file_path = "/var/www/html/mise/v0.1/logging/dacl-logs"
with open(file_path, "a") as file:
    # Append the output to the file
    file.write(time_string + "\n")
    file.write(result)



# Prepare the batch insert statement
insert_query = "INSERT INTO dacl (dacl, daclid, isename, get_code, href) VALUES (%s, %s, %s, %s, %s)"
insert_values = []

for resource in resources:
    try:
        my_id = resource['id']
        my_name = resource['name']
        srcauthurl = url + "/" + my_id
        href = resource['link']['href']        
        response2 = requests.get(srcauthurl, headers=headers, data=payload, verify=False)
        text_result = response2.text
        filename_web = initial_webfilename + my_id
        with open(filename_web, "w") as o:
            with contextlib.redirect_stdout(o):
                print(text_result)

        response_post = str(response2)
        response_post = response_post[:-1]
        response_post = response_post[1:]
        insert_values.append((my_name, my_id, fqdn, response_post,href))
        
    except IndexError:
        break

# Batch insert the data
cursor.executemany(insert_query, insert_values)
connection.commit()

# Delete query
delete_query = """
    DELETE t1 FROM dacl t1
    INNER JOIN dacl t2 ON CONCAT(t1.daclid, t1.isename) = CONCAT(t2.daclid, t2.isename)
    WHERE t1.id < t2.id
"""

#print("Generated DELETE query:")
#print(delete_query)

# Execute delete query
cursor.execute(delete_query)
connection.commit()


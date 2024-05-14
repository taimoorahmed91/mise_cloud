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


url = sys.argv[1]
my_id = sys.argv[2]

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

initial_webfilename = "/var/www/html/mise/v0.1/configs/sgt/"

      
response2 = requests.get(url, headers=headers, data=payload, verify=False)
text_result = response2.text
filename_web = initial_webfilename + my_id
with open(filename_web, "w") as o:
  with contextlib.redirect_stdout(o):
    print(text_result)



file_path = "/var/www/html/mise/v0.1/logging/sgt-logs"
with open(file_path, "a") as file:
    # Append the output to the file
    file.write(time_string + "\n")
    file.write(text_result)

response_post = str(response2)
response_post = response_post[:-1]
response_post = response_post[1:]
print(response_post)


cursor = connection.cursor(dictionary=True)
sql_update_query = """Update sgt set get_code = %s where sgtid = %s"""
input_data = (response_post, my_id)
cursor.execute(sql_update_query, input_data)
connection.commit()

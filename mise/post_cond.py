import urllib3
import requests
import sys
import json
import mysql.connector
import contextlib
import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


connection = mysql.connector.connect(host='127.0.0.1',
                                     database='mise',
                                     user='root',
                                     password='C1sc0123@')

#will accept id , dstise and dstpolicysetid

insertid = sys.argv [1]
fqdn = sys.argv[2]
condid = sys.argv[3]
cond = sys.argv[4]
isename = sys.argv[5]



### set time parameters
current_time = datetime.datetime.now()

# Format the time as a string
time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")




firsthalfurl = "https://"
secondhalfurl = "/api/v1/policy/network-access/condition"


url = firsthalfurl + fqdn + secondhalfurl 

#print(url)


## open the file as fetched from the SQL data

payload={}
#headers = {
#          'Content-Type': 'application/json',
#  'Accept': 'application/json',
#  'Authorization': 'Basic YWRtaW46QzFzYzAxMjNA',
#}

with open('credentials.txt') as file:
    # Execute the code in a separate namespace
    namespace = {}
    exec(file.read(), namespace)
    
    # Extract the 'headers' variable
    headers = namespace.get('headers', {})


filename = "/var/www/html/mise/v0.1/configs/condition/" + condid
#print(filename)

with open(f'{filename}', 'r', encoding='utf-8') as f:
    final_result = f.read()

#print(final_result)


response_post = requests.request("POST", url, headers=headers, data=final_result, verify=False)
output = (response_post.text)
print(output)


file_path = "/var/www/html/mise/v0.1/logging/cond-logs"
with open(file_path, "a") as file:
    # Append the output to the file
    file.write(time_string + "\n")
    file.write(output)



#json_response = response_post.json()
#print(json_response)


response_post = str(response_post)
response_post = response_post[:-1]
response_post = response_post[1:]
#print(response_post)
if response_post == "Response [201]":
    print("Success! Value is Response [201]. Exiting.")
    exit()
output2 = json.loads(output)

extracted_value = output2.get("message", "")  # Get the "message" field, or an empty string if it doesn't exist


cursor = connection.cursor(dictionary=True)
sql_insert_query = """INSERT INTO deploymentcode (element, type, action, code, output, dstise, srcise) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
input_data = (cond, 'Condition','POST',response_post,extracted_value,fqdn,isename)
cursor.execute(sql_insert_query, input_data)
connection.commit()
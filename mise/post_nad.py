import urllib3
import requests
import sys
import json
import mysql.connector
import contextlib
import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


connection = mysql.connector.connect(host='database',
                                     database='mise',
                                     user='root',
                                     password='C1sc0123@')

#will accept id , dstise and dstpolicysetid

insertid = sys.argv [1]
fqdn = sys.argv[2]
nadid = sys.argv[3]
nad = sys.argv[4]
isename = sys.argv[5]


### set time parameters
current_time = datetime.datetime.now()

# Format the time as a string
time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")




firsthalfurl = "https://"
secondhalfurl = "/ers/config/networkdevicegroup"


url = firsthalfurl + fqdn + secondhalfurl 

#print(url)


## open the file as fetched from the SQL data

payload={}
#headers = {
#          'Content-Type': 'application/json',
#  'Accept': 'application/json',
#  'Authorization': 'Basic YWRtaW46QzFzYzAxMjNA',
#}

with open('/var/www/html/mise/v0.1/credentials.txt') as file:
    # Execute the code in a separate namespace
    namespace = {}
    exec(file.read(), namespace)
    
    # Extract the 'headers' variable
    headers = namespace.get('headers', {})


filename = "/var/www/html/mise/v0.1/configs/nad/" + nadid
#print(filename)

with open(f'{filename}', 'r', encoding='utf-8') as f:
    final_result = f.read()

#print(final_result)


response_post = requests.request("POST", url, headers=headers, data=final_result, verify=False)
output = (response_post.text)
#print(output)


file_path = "/var/www/html/mise/v0.1/logging/nad-logs"
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

error_message = output2["ERSResponse"]["messages"][0]["title"]
second_last_dot_index = error_message.rfind(".", 0, error_message.rfind(".") - 1)
extracted_value = error_message[:second_last_dot_index].strip()


cursor = connection.cursor(dictionary=True)
sql_insert_query = """INSERT INTO deploymentcode (element, type, action, code, output, dstise, srcise) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
input_data = (nad, 'NAD Group','POST',response_post,extracted_value,fqdn,isename)
cursor.execute(sql_insert_query, input_data)
connection.commit()
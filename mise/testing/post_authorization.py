import urllib3
import requests
import sys
import json
import mysql.connector
import contextlib
import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#will accept fqdn 


insertid  = sys.argv[1]
fqdn  = sys.argv[2]
authorizationid = sys.argv[3]

connection = mysql.connector.connect(host='127.0.0.1',
                                     database='mise',
                                     user='root',
                                     password='C1sc0123@')


sql_select_Query = "select * from policysetdeploy ORDER BY id DESC LIMIT 1"

cursor = connection.cursor(dictionary=True)
cursor.execute(sql_select_Query)
records = cursor.fetchall()


for row in records:
        selectedpolicyset = row["selectedpolicyset"]

#print(selectedpolicyset)




### set time parameters
current_time = datetime.datetime.now()

# Format the time as a string
time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")



firsthalfurl = "https://"
secondhalfurl = "/api/v1/policy/network-access/policy-set"


url = firsthalfurl + fqdn + secondhalfurl 

print(url)

payload={}
headers = {
          'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Basic YWRtaW46QzFzYzAxMjNA',
}
response = requests.get(url, headers=headers, data=payload, verify=False)

json_response = response.json()


#print(json.dumps(json_response))


for value in json_response['response']:
    if value['name'] == selectedpolicyset:
        my_id=(value['id'])

#print(my_id)


authorization = "authorization"

newurl = url + "/" + my_id + "/" + authorization
#print(newurl)


filename = "/root/ise-landscape/mise/configs/authorizations/" + authorizationid
#print(filename)





with open(f'{filename}', 'r', encoding='utf-8') as f:
    final_result = f.read()

#print(final_result)


response_post = requests.request("POST", newurl, headers=headers, data=final_result, verify=False)
output = (response_post.text)
print(output)


file_path = "/var/www/html/landscape/logging/authorization-logs"
with open(file_path, "a") as file:
    # Append the output to the file
    file.write(time_string + "\n")
    file.write(output)

response_post = str(response_post)
response_post = response_post[:-1]
response_post = response_post[1:]
#print(response_post)


cursor = connection.cursor(dictionary=True)
sql_update_query = """Update authorization set post_code = %s where id = %s"""
input_data = (response_post,insertid )
cursor.execute(sql_update_query, input_data)
connection.commit()


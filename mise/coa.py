import urllib3
import requests
import sys
import json
import mysql.connector
import contextlib
import datetime
import xml.etree.ElementTree as ET
 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

fqdn = sys.argv[1]
mac = sys.argv[2]

url1 = "https://"
url2 = "/api/v1/deployment/node"
url = url1 + fqdn + url2

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
 #   print(node)
 #   print(services)
    if 'Session' in services:  # Note the case-sensitivity here
        # Construct the URL and store it in the 'url' variable
        url2 = f"https://{fqdn}/admin/API/mnt/CoA/Reauth/{node}/{mac}/1"
        break
print(url2)

headers2 = {
  'Authorization': 'Basic YWRtaW46QzFzYzAxMjNA'

}
response2 = requests.request("GET", url2, headers=headers2, data=payload, verify=False)
#print(response2)


response3 = str(response2)
response3 = response3[:-1]
response3 = response3[1:]
print(response3)

root = ET.fromstring(response2.content)
internal_error_info = root.find(".//internal-error-info").text


error_parts = internal_error_info.split(".")
if len(error_parts) >= 1:
    error_code = error_parts[0]
    print(f"Error Code: {error_code}")


#print(f"internal-error-info: {internal_error_info}")



connection = mysql.connector.connect(host='127.0.0.1',
                                     database='mise',
                                     user='root',
                                     password='C1sc0123@')



cursor = connection.cursor(dictionary=True)
sql_insert_query = """INSERT INTO coahistory (mac, url, response, message) VALUES (%s, %s, %s, %s)"""
input_data = (mac, fqdn,response3,error_code)
cursor.execute(sql_insert_query, input_data)
connection.commit()
import subprocess
import sys
import urllib3
import requests
import json
import mysql.connector
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)




# will accept only fqdn and run all things that were added to queue
# Script to fetch policyset authentication
mac = sys.argv[1]
print(mac)


connection = mysql.connector.connect(host='127.0.0.1',
                                     database='mise',
                                     user='root',
                                     password='C1sc0123@')




# Process coa
query_coa = "SELECT fqdn FROM deployments WHERE reachable = 'yes'"
# Execute your query and retrieve the results
cursor = connection.cursor(dictionary=True)
cursor.execute(query_coa)
results = cursor.fetchall()

for row in results:
    isename = row['fqdn']
    subprocess.run(['sudo', '-S', 'python3', '/root/ise-landscape/mise/coa.py', isename, mac], check=True)
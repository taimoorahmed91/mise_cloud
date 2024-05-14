import subprocess
import sys
import urllib3
import requests
import json
import mysql.connector
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)




# will accept only fqdn and run all things that were added to queue
# Script to fetch policyset authentication
fqdn = sys.argv[1]
print(fqdn)


connection = mysql.connector.connect(host='127.0.0.1',
                                     database='mise',
                                     user='root',
                                     password='C1sc0123@')




# Process dacl
query_dacl = "SELECT id, dacl, daclid, isename FROM dacl WHERE queue = 'yes'"
# Execute your query and retrieve the results
cursor = connection.cursor(dictionary=True)
cursor.execute(query_dacl)
results = cursor.fetchall()

for row in results:
    id = row['id']
    dacl = row['dacl']
    daclid = row['daclid']
    isename = row['isename']
    subprocess.run(['sudo', '-S', 'python3', '/root/ise-landscape/mise/post_dacl.py', str(id), fqdn, daclid, dacl, isename], check=True)

# Process authz
query_authz = "SELECT id, authz, authzid, isename FROM authz WHERE queue = 'yes'"
# Execute your query and retrieve the results

cursor = connection.cursor(dictionary=True)
cursor.execute(query_authz)
results = cursor.fetchall()

for row in results:
    id = row['id']
    authz = row['authz']
    authzid = row['authzid']
    isename = row['isename']
    subprocess.run(['sudo', '-S', 'python3', '/root/ise-landscape/mise/post_authz.py', str(id), fqdn, authzid, authz, isename], check=True)

# Process ap
query_ap = "SELECT id, ap, apid, isename FROM ap WHERE queue = 'yes'"
# Execute your query and retrieve the results
cursor = connection.cursor(dictionary=True)
cursor.execute(query_ap)
results = cursor.fetchall()


for row in results:
    id = row['id']
    ap = row['ap']
    apid = row['apid']
    isename = row['isename']
    subprocess.run(['sudo', '-S', 'python3', '/root/ise-landscape/mise/post_ap.py', str(id), fqdn, apid, ap, isename], check=True)

# Process nad
query_nad = "SELECT id, nad, nadid, isename FROM nad WHERE queue = 'yes'"
# Execute your query and retrieve the results
cursor = connection.cursor(dictionary=True)
cursor.execute(query_nad)
results = cursor.fetchall()

for row in results:
    id = row['id']
    nad = row['nad']    
    nadid = row['nadid']
    isename = row['isename']
    subprocess.run(['sudo', '-S', 'python3', '/root/ise-landscape/mise/post_nad.py', str(id), fqdn, nadid, nad, isename], check=True)

# Process sgt
query_sgt = "SELECT id, sgt, sgtid, isename FROM sgt WHERE queue = 'yes'"
# Execute your query and retrieve the results
cursor = connection.cursor(dictionary=True)
cursor.execute(query_sgt)
results = cursor.fetchall()


for row in results:
    id = row['id']
    sgt = row['sgt']
    sgtid = row['sgtid']
    isename = row['isename']
    subprocess.run(['sudo', '-S', 'python3', '/root/ise-landscape/mise/post_sgt.py', str(id), fqdn, sgtid, sgt, isename], check=True)




# Process condition
query_sgt = "SELECT id, cond, condid, isename FROM cond WHERE queue = 'yes'"
# Execute your query and retrieve the results
cursor = connection.cursor(dictionary=True)
cursor.execute(query_sgt)
results = cursor.fetchall()


for row in results:
    id = row['id']
    cond = row['cond']
    condid = row['condid']
    isename = row['isename']
    subprocess.run(['sudo', '-S', 'python3', '/root/ise-landscape/mise/post_cond.py', str(id), fqdn, condid, cond, isename], check=True)



# Process policyset
query_policyset = "SELECT id, policyset, policysetid, isename FROM policyset WHERE queue = 'yes'"
# Execute your query and retrieve the results
cursor = connection.cursor(dictionary=True)
cursor.execute(query_policyset)
results = cursor.fetchall()


for row in results:
    id = row['id']
    policyset = row['policyset']
    policysetid = row['policysetid']
    isename = row['isename']
    subprocess.run(['sudo', '-S', 'python3', '/root/ise-landscape/mise/post_policyset.py', str(id), fqdn, policysetid, policyset, isename], check=True)




# Process authentication
query_authentication = "SELECT id, authentication, authenticationid, isename FROM authentication WHERE queue = 'yes'"
# Execute your query and retrieve the results
cursor = connection.cursor(dictionary=True)
cursor.execute(query_authentication)
results = cursor.fetchall()


for row in results:
    id = row['id']
    authentication = row['authentication']
    authenticationid = row['authenticationid']
    isename = row['isename']
    subprocess.run(['sudo', '-S', 'python3', '/root/ise-landscape/mise/post_authentication.py', str(id), fqdn, authenticationid, authentication, isename], check=True)


# Process authentication
query_authentication = "SELECT id, authorization, authorizationid, isename FROM authorization WHERE queue = 'yes'"
# Execute your query and retrieve the results
cursor = connection.cursor(dictionary=True)
cursor.execute(query_authentication)
results = cursor.fetchall()


for row in results:
    id = row['id']
    authorization = row['authorization']
    authorizationid = row['authorizationid']
    isename = row['isename']
    subprocess.run(['sudo', '-S', 'python3', '/root/ise-landscape/mise/post_authorization.py', str(id), fqdn, authorizationid, authorization, isename], check=True)
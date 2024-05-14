import sys
import os
import mysql.connector

import urllib3
import requests

import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


id = sys.argv[1]
dstise = sys.argv[2]
name = sys.argv[3]

#print(f"Hello There: {id} and the destination ISE was {dstise} with {name} ")

# Base directory path
base_dir = "/var/www/html/mise/v0.1/configs/dacl/"

# Construct the file paths
file_path = os.path.join(base_dir, id)

# Open and read the file
try:
    with open(file_path, 'r') as file:
        file_contents = file.read()
        #print("File contents:")
        #print(file_contents)
except FileNotFoundError:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"An error occurred while opening the file: {e}")

# Print the file paths
#print(f"File Path: {file_path}")



payload = {}
with open('credentials.txt') as file:
    # Execute the code in a separate namespace
    namespace = {}
    exec(file.read(), namespace)
    
    # Extract the 'headers' variable
    headers = namespace.get('headers', {})

#create fqdn or URL put
url1 = "https://"
url2 = "/ers/config/downloadableacl/"

initial_url = url1 + dstise + url2
#print(initial_url)



# Existing script code...

# Database connection details (modify as necessary)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'C1sc0123@',
    'database': 'mise'
}

# Connect to the database
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Define the SQL query
    query = "SELECT daclid FROM dacl WHERE dacl = %s AND isename = %s;"

    # Execute the query
    cursor.execute(query, (name,dstise))
    result = cursor.fetchone()

    # Check and print the result
    if result:
        daclid = result[0]
        #print(f"DACL ID: {daclid}")
    else:
        print("No record found for the given name.")

    # Close the cursor and connection
    cursor.close()
    connection.close()

except mysql.connector.Error as error:
    print(f"Database error: {error}")


put_url = initial_url + daclid
#print(put_url)


#print(file_contents)



response_put = requests.request("PUT", put_url, headers=headers, data=file_contents, verify=False)
#print(response_put)


## updates to be pushed to db are from here

http_code = str(response_put)
http_code = http_code[:-1]
http_code = http_code[1:]
print(http_code)
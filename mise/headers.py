import mysql.connector
import base64

# Replace these values with your actual database credentials
db_config = {
    'host': '127.0.0.1',
    'database': 'mise',
    'user': 'root',
    'password': 'C1sc0123@'
}

# Establish a connection to the database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Execute the SELECT query
query = "SELECT `username`, `password` FROM `credentials`"
cursor.execute(query)

# Fetch the first row from the result set
row = cursor.fetchone()

if row:
    username = row[0]
    password = row[1]

    # Calculate base64 for the fetched credentials
    encoded_credentials = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")

    # Create the Authorization header
    authorization_header = f'Basic {encoded_credentials}'

    # Create the headers string
    headers = f"""headers = {{
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': '{authorization_header}',
}}
"""

    # Write the headers to the credentials.txt file
    credentials_file_path = '/root/ise-landscape/mise/credentials.txt'
    with open(credentials_file_path, 'w') as file:
        file.write(headers)

    print(f"Output written to '{credentials_file_path}' file.")
else:
    print("Failed to fetch credentials from the database.")

# Close the cursor and connection
cursor.close()
connection.close()

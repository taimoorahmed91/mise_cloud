import paramiko
import mysql.connector

def check_sftp_connection(host, port, username, password):
    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        transport.close()
        print("SFTP connection successful!")
    except Exception as e:
        print("SFTP connection failed:", str(e))

# Set the connection details
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="C1sc0123@",
    database="mise"
)

# Create a cursor
cursor = db_connection.cursor()

# Execute the SQL query
query = "SELECT name, uname, password FROM repo"
cursor.execute(query)

# Fetch all the results
results = cursor.fetchall()

# Close the database connection
db_connection.close()

# Iterate over the results
for row in results:
    host = row[0]
    username = row[1]
    password = row[2]

    print(f"Checking SFTP connection for host: {host}")

    # Check the SFTP connection
    check_sftp_connection(host, 22, username, password)
    print()

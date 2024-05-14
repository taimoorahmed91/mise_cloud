from webexteamssdk import WebexTeamsAPI
import requests
import sys
import mysql.connector

insertid = sys.argv[1]

#BOT_ACCESS_TOKEN = 'NmM3ZjliOTMtNjkyYi00ZWI1LTliNjItOGNhNWQ3YmJkYzQ2NWM2YWY5MzItMDA3_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f'


connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='C1sc0123@',
    database='mise'
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Execute the SQL query
query = "SELECT `token` FROM `webex`"
cursor.execute(query)

# Fetch the result
result = cursor.fetchone()

# Check if the result exists
if result:
    BOT_ACCESS_TOKEN = result[0]  # Extract the token from the result
    print("BOT_ACCESS_TOKEN:", BOT_ACCESS_TOKEN)
else:
    print("No token found in the database")

# Close the cursor and database connection
cursor.close()
connection.close()















URL = 'https://api.ciscospark.com/v1/messages'
MESSAGE_TEXT = ''

# Establish a connection to your MySQL database
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='C1sc0123@',
    database='mise'
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Execute the SQL query
query = "SELECT `fqdn`,`time` FROM `deployments` WHERE id = %s"
cursor.execute(query, (insertid,))

# Fetch the result
result = cursor.fetchone()


# Check if a result is available
if result:
    # Extract the values from the result
    fqdn, time = result

    # Build the message text
    MESSAGE_TEXT = "==============================================================\n" 
    MESSAGE_TEXT += "MISE has completed fetching your ISE deployment. Here are your results:\n\n"
    MESSAGE_TEXT += f"Deployment Name: {fqdn}\n"
    MESSAGE_TEXT += f"Populated Time: {time}\n\n"
    MESSAGE_TEXT += "This is an auto generated message, please do not reply to it.\n"
    MESSAGE_TEXT += "==============================================================\n"



# Close the database connection
connection.close()

# If no result was found, display a message indicating it
if not MESSAGE_TEXT:
    MESSAGE_TEXT = "No results found."

# Set up the headers for the API request
headers = {
    'Authorization': 'Bearer ' + BOT_ACCESS_TOKEN,
    'Content-type': 'application/json;charset=utf-8'
}

# Create a Webex Teams API object with your access token
api = WebexTeamsAPI(access_token=BOT_ACCESS_TOKEN)

# Get a list of all rooms in the account
rooms = api.rooms.list()
#print(rooms)






for room in rooms:
    # Check if room.title is equal to "Taimoor Ahmed"
    if room.title == "Taimoor Ahmed":
        #print(f"Room Name: {room.title}\nRoom ID: {room.id}\n")
        post_data = {'roomId': room.id, 'text': MESSAGE_TEXT}
        response = requests.post(URL, json=post_data, headers=headers)

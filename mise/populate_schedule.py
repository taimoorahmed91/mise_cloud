import mysql.connector
from datetime import datetime, timedelta
import subprocess

# Connect to the database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="C1sc0123@",
    database="mise"
)

# Create a cursor
cursor = db_connection.cursor()

# Execute the SQL query
cursor.execute("SELECT id, fqdn, hours, nextrun, lastrun FROM actionschedule WHERE action = 'populate'")

# Fetch all the results
results = cursor.fetchall()

# Save the results in variables
ids = []
fqdns = []
hours = []
nextruns = []
lastruns = []

# Get the current datetime
current_datetime = datetime.now()

for row in results:
    ids.append(row[0])
    fqdn = row[1].split("/")[0]  # Split the fqdn before saving
    fqdns.append(fqdn)
    hours.append(row[2])
    nextrun = row[3]
    nextruns.append(nextrun)
    lastrun = row[4]
    lastruns.append(lastrun)

    # Check if the nextrun is in the past
    if nextrun < current_datetime:
        print(f"Next run ({nextrun}) is in the past for ID {row[0]} and FQDN {fqdn}")

        # Convert hours to timedelta and calculate new_nextrun
        hours_offset = timedelta(hours=int(row[2]))
        new_nextrun = current_datetime + hours_offset

        # Update nextrun and lastrun in the database
        update_query = "UPDATE actionschedule SET nextrun = %s, lastrun = %s WHERE id = %s"
        new_values = (new_nextrun, current_datetime, row[0])
        cursor.execute(update_query, new_values)
        db_connection.commit()

        # Construct and print the URL
        url = f"https://localhost/mise/v0.1/populate.php?id={fqdn}"
        print(url)

        # Execute curl command with the URL
        subprocess.run(['curl', '-k', url])

        # Print the new nextrun value
        print(f"New Next run: {new_nextrun}")

# Close the database connection
db_connection.close()


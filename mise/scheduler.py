import time
import mysql.connector
import requests
from datetime import datetime


while True:
    # Establish a connection to the MySQL database
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="C1sc0123@",
        database="mise"
    )

    # Create a cursor to execute SQL queries
    cursor = db_connection.cursor()

    # Execute the SQL query
    cursor.execute("SELECT id, fqdn, frequency FROM scheduler")

    # Fetch all the results
    results = cursor.fetchall()

    # Iterate over the results
    for result in results:
        id = result[0]
        fqdn = result[1].split("/")[0]
        frequency = result[2]
        url = f"http://localhost/mise/v0.1/populate.php?id={fqdn}"
        print(url)

        # Update the scheduler column to 'yes' for the current row
        update_query = f"UPDATE scheduler SET scheduler = 'yes' WHERE id = {id}"
        cursor.execute(update_query)
        db_connection.commit()

        # Send a GET request to the URL
        response = requests.get(url)
        print(response.text)

        # Update the scheduler column back to 'no' for the current row
        update_query = f"UPDATE scheduler SET scheduler = 'no' WHERE id = {id}"
        cursor.execute(update_query)
        db_connection.commit()

                # Update the lastrun column with the current time
        update_query = f"UPDATE scheduler SET lastrun = '{datetime.now()}' WHERE id = {id}"
        cursor.execute(update_query)
        db_connection.commit()

    # Close the cursor and database connection
    cursor.close()
    db_connection.close()

    # Sleep for the frequency in seconds
    time.sleep(frequency)

import mysql.connector
from datetime import datetime
import subprocess

connection = mysql.connector.connect(
    host='127.0.0.1',
    database='mise',
    user='root',
    password='C1sc0123@'
)

cursor = connection.cursor()
query = "SELECT time, now FROM deployschedule WHERE run ='no'"
cursor.execute(query)

results = cursor.fetchall()
if results:
    print('Fetched values:')
    current_time = datetime.now()
    for result in results:
        value = result[0]
        now_value = result[1]
        print('- Value:', value)
        if value < current_time:
            print('  The fetched time is in the past. Updating the database...')
            update_query = "UPDATE deployschedule SET now = 'yes' WHERE time = %s"
            cursor.execute(update_query, (value,))
            connection.commit()
            print('  Database updated successfully.')
            
            query = "SELECT now FROM deployschedule WHERE time = %s"
            cursor.execute(query, (value,))
            updated_result = cursor.fetchone()
            if updated_result and updated_result[0] == 'yes':
                print('  The "now" column is set to "yes". Running deploy.php...')
                # Run deploy.php using the curl command
                subprocess.run(['curl', '-k', 'https://localhost/mise/v0.1/deploy.php'])
                print('  deploy.php executed successfully. Updating the database...')
                update_query = "UPDATE deployschedule SET now = 'no', run = 'yes' WHERE time = %s"
                cursor.execute(update_query, (value,))
                connection.commit()
                print('  Database updated successfully.')
            else:
                print('  Error executing deploy.php or "now" column not set to "yes".')
        else:
            print('  The fetched time is not in the past.')
else:
    print('No values found')

cursor.close()
connection.close()

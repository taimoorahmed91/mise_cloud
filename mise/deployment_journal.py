import json
import mysql.connector
from datetime import datetime

# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='C1sc0123@',
    database='mise'
)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Define the SQL query
query = """
SELECT `ap` AS `name`, 'ap' AS `table_name` FROM ap WHERE `queue` = 'yes'
UNION ALL
SELECT `dacl` AS `name`, 'dacl' AS `table_name` FROM dacl WHERE `queue` = 'yes'

UNION ALL
SELECT `authz` AS `name`, 'authz' AS `table_name` FROM authz WHERE `queue` = 'yes'

UNION ALL
SELECT `sgt` AS `name`, 'sgt' AS `table_name` FROM sgt WHERE `queue` = 'yes'

UNION ALL
SELECT `nad` AS `name`, 'nad' AS `table_name` FROM nad WHERE `queue` = 'yes'

UNION ALL
SELECT `cond` AS `name`, 'cond' AS `table_name` FROM cond WHERE `queue` = 'yes'


UNION ALL
SELECT `policyset` AS `name`, 'policyset' AS `table_name` FROM policyset WHERE `queue` = 'yes'

UNION ALL
SELECT `authentication` AS `name`, 'authentication' AS `table_name` FROM authentication WHERE `queue` = 'yes'




UNION ALL
SELECT `fqdn` AS `name`, 'deployments' AS `table_name` FROM deployments WHERE `marked` = 'yes'








ORDER BY `table_name`;

"""

# Execute the SQL query
cursor.execute(query)

# Create a dictionary to store the table names and corresponding names
data = {}

# Fetch rows from the result and populate the data dictionary
for row in cursor.fetchall():
    name = row[0]
    table_name = row[1]
    
    if table_name not in data:
        data[table_name] = []
    
    data[table_name].append(name)

# Close the cursor and the database connection
cursor.close()
connection.close()

# Create a unique filename with date and time
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"/var/www/html/mise/v0.1/deployments/deployment_{timestamp}.json"

# Write the data to a file in JSON format with indentation
with open(filename, 'w') as file:
    json.dump(data, file, indent=4)

#print(f"Data written to {filename}")

#print(filename)
last_part = filename.split("/")[-1]
first = filename.split("/")[-2]

first_part = first + "/" + last_part

connection = mysql.connector.connect(host='127.0.0.1',
                                     database='mise',
                                     user='root',
                                     password='C1sc0123@')


sql_select_Query = "select * from policysetdeploy ORDER BY id DESC LIMIT 1"

cursor = connection.cursor(dictionary=True)
cursor.execute(sql_select_Query)
records = cursor.fetchall()


for row in records:
        comments = row["comments"]





connection = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='C1sc0123@',
    database='mise'
)
cursor = connection.cursor()


query = "INSERT INTO deployhistory (name,path,comments) VALUES (%s, %s, %s)"
values = (last_part , first_part, comments)
cursor.execute(query, values)
connection.commit()















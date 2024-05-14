import mysql.connector

# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='C1sc0123@',
    database='mise'
)

# Create a cursor to execute SQL queries
cursor = connection.cursor()

# Fetch all table names from the database
cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()

# Iterate through each table and update the "queue" column
for table in tables:
    table_name = table[0]
    update_query = f"UPDATE {table_name} SET queue = 'yes';"
    try:
        cursor.execute(update_query)
        connection.commit()
        print(f"Updated 'queue' column in table: {table_name}")
    except mysql.connector.Error as error:
        if error.errno == 1054:  # Error for unknown column 'queue'
            print(f"Skipping table '{table_name}' as 'queue' column does not exist.")
        else:
            print(f"Error updating table '{table_name}': {error}")
        connection.rollback()

# Close the cursor and connection
cursor.close()
connection.close()


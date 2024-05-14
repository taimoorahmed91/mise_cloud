import mysql.connector
import sys
import os
import subprocess



# Get the ID from command line arguments
id = sys.argv[1]

# Establish a connection to your MySQL database
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='C1sc0123@',
    database='mise'
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Define the first SQL query, using the ID from the command line
first_query = "SELECT * FROM deploymentcode WHERE id = %s;"

try:
    # Execute the first query with the provided ID
    cursor.execute(first_query, (id,))

    # Fetch all the rows
    rows = cursor.fetchall()

    # Initialize variables to store final results
    final_results_second_query = ""
    final_results_third_query = ""

    # Check if any rows are returned
    if rows:
        # Assuming there's only one row since we're querying by a unique ID
        row = rows[0]

        # Extracting the required fields
        element = row[1]
        type_field = row[2].lower()  # Convert type_field to lowercase
        srcise = row[6]
        dstise = row[7]

        # Create a new variable by appending "id" to type_field
        type_id = type_field + "id"

        # Define and execute the second query
        second_query = f"SELECT {type_id} FROM {type_field} WHERE {type_field} = %s AND isename = %s;"
        cursor.execute(second_query, (element, srcise))

        # Fetch and process all the rows from the second query
        second_query_rows = cursor.fetchall()
        for row in second_query_rows:
            final_results_second_query += f"{row[0]}, "

        # Define and execute the third query, using dstise
        third_query = f"SELECT {type_id} FROM {type_field} WHERE {type_field} = %s AND isename = %s;"
        cursor.execute(third_query, (element, dstise))

        # Fetch and process all the rows from the third query
        third_query_rows = cursor.fetchall()
        for row in third_query_rows:
            final_results_third_query += f"{row[0]}, "

    else:
        print("No data found for the specified ID.")

except mysql.connector.Error as error:
    print(f"Error: {error}")

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()

# Save the cleaned-up results in new variables
src_id = final_results_second_query.rstrip(", ")
dst_id = final_results_third_query.rstrip(", ")

# Print the cleaned-up results
#print(src_id)
#print(dst_id)

# Print the cleaned-up results
print(f"ID of Element 1: {src_id}")
print(f"ID of Element 2: {dst_id}")

# Base directory path
base_dir = "/var/www/html/mise/v0.1/configs"

# Construct the file paths
src_file_path = os.path.join(base_dir, type_field, src_id)
dst_file_path = os.path.join(base_dir, type_field, dst_id)

# Print the file paths
#print(src_file_path)
#print(dst_file_path)

print("\n\n")
print("\n")



# Run compare.py as a subprocess with sudo
compare_command = ["sudo", "-S", "python3", "/root/ise-landscape/mise/compare.py", src_file_path, dst_file_path]
result = subprocess.run(compare_command, capture_output=True, text=True)

# Print the output of compare.py
print(result.stdout)

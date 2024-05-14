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


# Print the cleaned-up results
#print(src_id)

# Print Type field to check what element type it is
#print(type_field)


script_element = "put_" + type_field + ".py"
#print(script_element)


script_element1 = os.path.join("/root/ise-landscape/mise/", script_element)



# Construct the command with sudo, Python 3, script name, and the argument
command = ["sudo", "-S", "python3", script_element1, src_id, dstise, element]

# Execute the command using subprocess and capture the output
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Save the output (and potentially error) in variables
output = result.stdout
error = result.stderr

# Print the output and error
print("Output:", output)
#print("Error:", error if error else "No error")



# Check the output and update the database if necessary
if "Response [200]" in output:
    try:
        # Re-establish the database connection
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='C1sc0123@',
            database='mise'
        )
        cursor = connection.cursor()

        # Prepare the update query
        update_query = "UPDATE deploymentcode SET output = 'Element overwritten successfully' WHERE id = %s;"

        # Execute the update query
        cursor.execute(update_query, (id,))

        # Commit the changes to the database
        connection.commit()

        print("Database updated successfully.")

    except mysql.connector.Error as error:
        print(f"Database update error: {error}")

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()
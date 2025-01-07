import sqlite3
import os
import operation
import operation.dboperation

# Get the absolute path to the database file
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "./dbs/university.db"))

# Create a connection to the database
conn = operation.dboperation.create_connection()
mycursor = conn.cursor()

# Query to list all tables in the database
mycursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Fetch all results
tables = mycursor.fetchall()

# Print the table names
print("Tables in the database:")
for table in tables:
    print(table[0])

# Close the cursor and connection
mycursor.close()
conn.close()


#altering the table 



import sqlite3
import pandas as pd

# Function to connect to the SQLite database
def connect_to_db(db_file):
    conn = sqlite3.connect(db_file)
    return conn

# Function to execute a query and fetch results
def execute_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

# Connect to the SQLite database
conn = connect_to_db('stackoverflow_users_database_for_test.db')

# Query to fetch all rows from the users table
select_query = "SELECT * FROM users"
rows_result = execute_query(conn, select_query)

# Close the database connection
conn.close()

# Create DataFrame
df = pd.DataFrame(rows_result, columns=['user_id', 'display_name', 'reputation', 'gold_badges', 'silver_badges'])

# Print DataFrame
print("DataFrame:")
print(df)

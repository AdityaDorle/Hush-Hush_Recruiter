import sqlite3
import pandas as pd

# Connect to the 'developers_for_all.db' database
conn = sqlite3.connect('developers_for_all.db')

# Read the contents of the 'developer_s' table into a DataFrame
query_s = "SELECT * FROM developer_s"
df_s = pd.read_sql_query(query_s, conn)

# Read the contents of the 'developer_g' table into a DataFrame
query_g = "SELECT * FROM developer_g"
df_g = pd.read_sql_query(query_g, conn)

# Close the database connection
conn.close()

# Display the contents of the 'developer_s' table
print("Contents of 'developer_s' table:")
print(df_s)

# Display the contents of the 'developer_g' table
print("\nContents of 'developer_g' table:")
print(df_g)

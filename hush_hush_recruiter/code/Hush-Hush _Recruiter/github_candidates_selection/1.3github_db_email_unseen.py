import sqlite3
import pandas as pd
import random
import string

# Function to generate a random email address based on the username
def generate_email(username):
    domain = '@example.com'  # You can replace this with your desired domain
    username = username.lower().replace(' ', '')  # Convert username to lowercase and remove spaces
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=5))  # Generate a random string
    return f"{username}{random_str}{domain}"

# Read the JSON file into a DataFrame
df = pd.read_json('output_data_barai_test.json')

# Check if 'email' is null and generate random email if so
df['email'] = df.apply(lambda row: generate_email(row['username']) if pd.isnull(row['email']) else row['email'], axis=1)

# Connect to the SQLite3 database
conn = sqlite3.connect('unseen_data_base.db')

# Write the DataFrame to the database
df.to_sql('unseen_table_name', conn, if_exists='replace', index=False)  # Replace 'your_table_name' with the desired table name

# Commit changes and close the connection
conn.commit()
conn.close()

import sqlite3
import pandas as pd

# Connect to the SQLite3 database
conn = sqlite3.connect('unseen_data_base.db')

# Query to select all records from your table
query = "SELECT * FROM unseen_table_name"  # Replace 'your_table_name' with the actual table name

# Execute the query and fetch all records
all_data = pd.read_sql_query(query, conn)

# Display the data
print(all_data)

# Close the connection
conn.close()


import sqlite3
import pandas as pd

# Read the JSON file into a DataFrame
df = pd.read_json('output_data_barai_test.json')

# Connect to the SQLite3 database
conn = sqlite3.connect('unseen_data_base.db')

# Write the DataFrame to the database
df.to_sql('unseen_table_name', conn, if_exists='replace', index=False)  # Replace 'your_table_name' with the desired table name

# Commit changes and close the connection
conn.commit()
conn.close()

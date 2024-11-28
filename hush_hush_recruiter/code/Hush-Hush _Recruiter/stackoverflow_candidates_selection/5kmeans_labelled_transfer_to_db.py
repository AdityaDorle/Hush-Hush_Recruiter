import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('converted_database.db')

# Execute a query to retrieve data for good candidates
good_candidates_query = "SELECT * FROM candidates WHERE candidate_type = 'good'"
good_candidates_df = pd.read_sql_query(good_candidates_query, conn)

print("Good Candidates:")
print(good_candidates_df)


bad_candidates_query = "SELECT * FROM candidates WHERE candidate_type = 'bad'"
bad_candidates_df = pd.read_sql_query(bad_candidates_query, conn)

print("bad Candidates:")
print(bad_candidates_df)

# Close the connection
conn.close()
# Close the connection
conn.close()

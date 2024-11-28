import sqlite3
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

# Function to generate a random email using the username
def generate_email(username):
    return f"{username.lower()}@example.com"

# Connect to SQLite3 database
conn = sqlite3.connect('github_data_all.db')

# Read data from the database into a DataFrame
df = pd.read_sql_query("SELECT * FROM all_candidates", conn)

# Close connection
conn.close()

# Replace 'None' values in 'email' column with randomly generated emails
df['email'] = df.apply(lambda row: generate_email(row['username']) if row['email'] is None else row['email'], axis=1)

# Drop non-numeric columns
df_numeric = df.drop(['username', 'email'], axis=1)

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_numeric)

# Perform DBSCAN clustering with best parameters
dbscan = DBSCAN(eps=0.5, min_samples=5)
df['cluster'] = dbscan.fit_predict(X_scaled)

# Label clusters -1 as "good" and cluster 0 as "bad"
df['category'] = df['cluster'].map({-1: 'good', 0: 'bad'})

# Print the updated DataFrame with categories
print("Updated DataFrame with Categories:")
print(df)

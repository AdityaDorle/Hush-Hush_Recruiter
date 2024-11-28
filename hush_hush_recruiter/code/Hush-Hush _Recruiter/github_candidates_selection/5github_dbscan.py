
import sqlite3
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.model_selection import ParameterGrid

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

# Define parameter grid
param_grid = {'eps': [0.1, 0.5, 1.0, 1.5],
              'min_samples': [3, 5, 10, 15]}

best_score = -1
best_params = None

# Perform grid search
for params in ParameterGrid(param_grid):
    dbscan = DBSCAN(**params)
    cluster_labels = dbscan.fit_predict(X_scaled)
    silhouette_avg = silhouette_score(X_scaled, cluster_labels)
    if silhouette_avg > best_score:
        best_score = silhouette_avg
        best_params = params

# Perform DBSCAN clustering with best parameters
dbscan = DBSCAN(**best_params)
df['cluster'] = dbscan.fit_predict(X_scaled)

# Calculate silhouette score
print("Best Silhouette Score:", best_score)
print("Results of All Candidates:")
print(df)
# Count the number of candidates in each cluster
cluster_counts = df['cluster'].value_counts()

# Print the count of candidates in each cluster
print("Number of Candidates in Each Cluster:")
print(cluster_counts)

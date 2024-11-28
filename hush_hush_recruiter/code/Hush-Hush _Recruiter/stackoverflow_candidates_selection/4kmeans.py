import sqlite3
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score  # Import silhouette_score

# Function to connect to the SQLite database and retrieve data
def retrieve_data_from_db(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    result = cursor.fetchone()
    if result:
        query = "SELECT * FROM users"
        df = pd.read_sql_query(query, conn)
    else:
        df = None
    conn.close()
    return df

# Connect to the SQLite database and retrieve data
df = retrieve_data_from_db('stackoverflow_users_database.db')

if df is not None:
    print("Data from database:")
    print(df.head())

    # Apply KMeans algorithm
    kmeans = KMeans(n_clusters=2, random_state=42)  # Assuming we want to distinguish between 2 categories: good and bad
    kmeans.fit(df[['reputation', 'gold_badges', 'silver_badges']])

    # Calculate silhouette score
    silhouette_avg = silhouette_score(df[['reputation', 'gold_badges', 'silver_badges']], kmeans.labels_)
    print("Silhouette Score:", silhouette_avg)  # Print silhouette score

    # Add cluster labels to the DataFrame
    df['cluster_label'] = kmeans.labels_

    # Calculate cluster centroids
    centroids = pd.DataFrame(kmeans.cluster_centers_, columns=['reputation', 'gold_badges', 'silver_badges'])

    print("\nCentroids:")
    print(centroids)

    # Define criteria for good and bad candidates based on cluster centroids
    # We assume that the cluster with higher reputation and badge counts is "good"
    good_criteria = centroids.idxmax(axis=0)
    bad_criteria = centroids.idxmin(axis=0)

    print("\nGood Criteria:")
    print(good_criteria)
    print("\nBad Criteria:")
    print(bad_criteria)

    # Label candidates as "good" or "bad" based on the criteria
    df['candidate_type'] = 'bad'
    for criterion, value in good_criteria.items():
        df.loc[df[criterion] >= centroids.iloc[1][criterion], 'candidate_type'] = 'good'

    # Display the DataFrame with candidate types
    print("\nFinal DataFrame:")
    print(df[['reputation', 'gold_badges', 'silver_badges', 'candidate_type']].head(10))
else:
    print("The 'users' table does not exist in the database.")

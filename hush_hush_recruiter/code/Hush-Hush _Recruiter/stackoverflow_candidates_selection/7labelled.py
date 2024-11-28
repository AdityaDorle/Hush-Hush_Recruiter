import sqlite3
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

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

    # Feature scaling
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[['reputation', 'gold_badges', 'silver_badges']])
    df_scaled = pd.DataFrame(scaled_features, columns=['reputation', 'gold_badges', 'silver_badges'])

    # Apply KMeans algorithm
    kmeans = KMeans(n_clusters=2, random_state=42)  # Assuming we want to distinguish between 2 categories: good and bad
    kmeans.fit(df_scaled)

    # Add cluster labels to the DataFrame
    df['cluster_label'] = kmeans.labels_

    # Calculate cluster centroids
    centroids = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=['reputation', 'gold_badges', 'silver_badges'])

    # Check cluster distribution
    print("Cluster distribution:")
    print(df['cluster_label'].value_counts())

    # Inspect centroids
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

    # Evaluate the distribution of candidate types
    print("\nDistribution of candidate types:")
    print(df['candidate_type'].value_counts())
    
else:
    print("The 'users' table does not exist in the database.")
# Print the list of good candidates
print("List of Good Candidates:")
good_candidates = df[df['candidate_type'] == 'good']
print(good_candidates)

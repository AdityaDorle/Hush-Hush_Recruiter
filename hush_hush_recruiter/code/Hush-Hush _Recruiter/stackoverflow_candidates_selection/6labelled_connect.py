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

    # Define criteria for good and bad candidates based on cluster centroids
    # We assume that the cluster with higher reputation and badge counts is "good"
    good_criteria = centroids.idxmax(axis=0)
    bad_criteria = centroids.idxmin(axis=0)

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

    # Connect to the SQLite database
    conn = sqlite3.connect('converted_database.db')

    # Save the DataFrame to the SQLite database as a new table
    df.to_sql('candidates', conn, index=False, if_exists='replace')

    # Execute a query to retrieve data for good candidates
    good_candidates_query = "SELECT * FROM candidates WHERE candidate_type = 'good'"
    good_candidates_df = pd.read_sql_query(good_candidates_query, conn)

    print("\nGood Candidates:")
    print(good_candidates_df)

    # Execute a query to retrieve data for bad candidates
    bad_candidates_query = "SELECT * FROM candidates WHERE candidate_type = 'bad'"
    bad_candidates_df = pd.read_sql_query(bad_candidates_query, conn)

    print("\nBad Candidates:")
    print(bad_candidates_df)

    # Close the connection
    conn.close()
else:
    print("The 'users' table does not exist in the database.")

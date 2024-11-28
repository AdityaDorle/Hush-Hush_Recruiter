import sqlite3
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import random
import string

# Load the trained RandomForestClassifier
model = joblib.load('random_forest_model.pkl')

# Connect to the SQLite database containing the unseen data
conn = sqlite3.connect('stackoverflow_users_database_for_test.db')

# Retrieve data from the 'users' table
query = "SELECT display_name, reputation, gold_badges, silver_badges FROM users"
unseen_df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Function to generate a random ID number
def generate_id(display_name):
    random_digits = ''.join(random.choices(string.digits, k=3))
    return display_name[:3].lower() + random_digits

# Function to generate a random email
def generate_email(display_name):
    domain = '@stackoverflow.com'
    return display_name.lower().replace(' ', '') + domain

# Add 'id_number' column to the DataFrame
unseen_df['id_number'] = unseen_df['display_name'].apply(generate_id)

# Add 'email' column to the DataFrame
unseen_df['email'] = unseen_df['display_name'].apply(generate_email)

# Standardize features by removing the mean and scaling to unit variance
scaler = StandardScaler()
X_unseen = unseen_df[['reputation', 'gold_badges', 'silver_badges']]
X_unseen_scaled = scaler.fit_transform(X_unseen)

# Make predictions on the unseen data
predictions = model.predict(X_unseen_scaled)

# Get probabilities of being "good"
probabilities = model.predict_proba(X_unseen_scaled)[:, 1]

# Add predictions and probabilities to the unseen DataFrame
unseen_df['predicted_category'] = predictions
unseen_df['probability_good'] = probabilities

# Select the top 10 candidates with their details
top_10_candidates = unseen_df.sort_values(by='probability_good', ascending=False).head(10)

# Connect to the 'developers_for_all.db' database
conn_all_developers = sqlite3.connect('developers_for_all.db')

# Write the top 10 candidates to the 'developer_s' table in the existing database
top_10_candidates.to_sql('developer_s', conn_all_developers, if_exists='replace', index=False)

# Close connection to the database
conn_all_developers.close()

# Display confirmation message
print("Top 10 Candidates stored in 'developer_s' table of 'developers_for_all.db' database.")

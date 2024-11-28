
import sqlite3
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle
import random
import string

# Load the saved model and data
with open('saved_model_and_data.pkl', 'rb') as file:
    saved_data = pickle.load(file)

# Access the model
model = saved_data['model']

# Connect to the 'unseen_data_base.db' database
conn_unseen = sqlite3.connect('unseen_data_base.db')

# Read unseen data from the specified table into a DataFrame
unseen_df = pd.read_sql_query("SELECT * FROM unseen_table_name", conn_unseen)

# Close connection to the unseen data database
conn_unseen.close()

# Generate unique IDs for the top 10 candidates
def generate_unique_id(username):
    random_suffix = ''.join(random.choices(string.digits, k=3))
    return username[:3] + random_suffix

unseen_df['unique_id'] = unseen_df['username'].apply(generate_unique_id)

# Separate features from the unseen data
X_unseen = unseen_df[['followers', 'number_of_repos', 'stars', 'forks', 'pull_number']]

# Standardize the features using the same scaler applied to the training data
scaler = StandardScaler()
X_unseen_scaled = scaler.fit_transform(X_unseen)

# Make predictions on the preprocessed unseen data
predictions_proba = model.predict_proba(X_unseen_scaled)

# Get the probabilities of being a "good" candidate
good_probs_unseen = predictions_proba[:, -1]

# Add predicted probabilities to the unseen DataFrame
unseen_df['predicted_probability'] = good_probs_unseen

# Filter the unseen DataFrame for top 10 candidates
top_10_candidates_unseen = unseen_df.sort_values(by='predicted_probability', ascending=False).head(10)

# Connect to the 'developers_for_all.db' database
conn_developers_for_all = sqlite3.connect('developers_for_all.db')

# Write the top 10 selected candidates to the 'developer_g' table in the new database
top_10_candidates_unseen.to_sql('developer_g', conn_developers_for_all, if_exists='replace', index=False)

# Close connection to the new database
conn_developers_for_all.close()

# Display confirmation message
print("Top 10 Selected Candidates stored in 'developer_g' table of 'developers_for_all.db' database.")

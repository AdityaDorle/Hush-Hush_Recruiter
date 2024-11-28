
import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib  # Import joblib for saving the model
  # Import joblib for saving the model

# Connect to the SQLite database
conn = sqlite3.connect('converted_database.db')

# Retrieve data from the database
query = "SELECT * FROM candidates"
df = pd.read_sql_query(query, conn)

# Close the connection
conn.close()

# Separate features (X) and target variable (y)
X = df[['reputation', 'gold_badges', 'silver_badges']]
y = df['candidate_type']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features by removing the mean and scaling to unit variance
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize and train the random forest classifier
random_forest_model = RandomForestClassifier(n_estimators=100, random_state=42)
random_forest_model.fit(X_train_scaled, y_train)

# Save the trained model using joblib
joblib.dump(random_forest_model, 'random_forest_model.pkl')

# Predictions
y_pred = random_forest_model.predict(X_test_scaled)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

# Classification report
class_report = classification_report(y_test, y_pred)

print("Performance Parameters (Random Forest):")
print(f"Accuracy: {accuracy:.3f}\n")
print("Classification Report:")
print(class_report)

# Calculate probabilities of candidates being "good"
probabilities = random_forest_model.predict_proba(X_test_scaled)[:, 1]

# Add probabilities to the test set DataFrame
X_test_with_probabilities = X_test.copy()
X_test_with_probabilities['probability_good'] = probabilities

# Merge candidate names with their probabilities
top_candidates_with_names = pd.concat([X_test_with_probabilities, df.loc[X_test_with_probabilities.index, 'display_name']], axis=1)

# Sort candidates by their probability of being "good" in descending order
top_candidates_with_names_sorted = top_candidates_with_names.sort_values(by='probability_good', ascending=False)

# Select the top 5 candidates with display name, reputation count, both badges, and probability of being "good"
top_10_candidates_with_details = top_candidates_with_names_sorted.head(10)[['display_name', 'reputation', 'gold_badges', 'silver_badges', 'probability_good']]

print("\nTop 10 Candidates (Random Forest):")
print(top_10_candidates_with_details)

import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import classification_report
import pickle

# Connect to SQLite3 database
conn = sqlite3.connect('label_git_candidate.db')

# Read data from the database into a DataFrame
df = pd.read_sql_query("SELECT * FROM label_category_candidate", conn)

# Close connection
conn.close()

# Separate features and target variable
X = df[['followers', 'number_of_repos', 'stars', 'forks', 'pull_number']]  # Features
y = df['category']  # Target variable

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Initialize Random Forest classifier with best parameters from grid search
model = RandomForestClassifier(n_estimators=50, max_depth=None, min_samples_split=2, min_samples_leaf=2, random_state=42)

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train Random Forest model on the training set
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Compute classification report
classification_rep = classification_report(y_test, y_pred)

# Display classification report
print("Classification Report:")
print(classification_rep)

# Calculate and display average CV score
cv_size = 10  
cv_scores = cross_val_score(model, X_scaled, y, cv=cv_size)
print("Average CV Score:", cv_scores.mean())

# Get predicted probabilities for each class
y_pred_proba = model.predict_proba(X_scaled)

# Get the probabilities of being a "good" candidate
good_probs = y_pred_proba[:, 0]

# Add predicted probabilities to DataFrame
df['predicted_probability'] = good_probs

# Filter the DataFrame for "good" candidates
good_candidates_df = df[df['category'] == 'good']

# Sort "good" candidates by predicted probability (descending order)
good_candidates_sorted = good_candidates_df.sort_values(by='predicted_probability', ascending=False)

# Display top 10 "good" candidates
print("Top 10 Good Candidates:")
print(good_candidates_sorted.head(10))

# Store the trained model and DataFrame in a dictionary
saved_data = {
    'model': model,
    'df': df
}

# Save the dictionary using pickle
with open('saved_model_and_data.pkl', 'wb') as file:
    pickle.dump(saved_data, file)





# This below commented clode i used to find best grid parameter and used those parameter in the above code for best results

# import sqlite3
# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import GridSearchCV, train_test_split
# from sklearn.metrics import classification_report

# # Connect to SQLite3 database
# conn = sqlite3.connect('label_git_candidate.db')

# # Read data from the database into a DataFrame
# df = pd.read_sql_query("SELECT * FROM label_category_candidate", conn)

# # Close connection
# conn.close()

# # Separate features and target variable
# X = df[['followers', 'number_of_repos', 'stars', 'forks', 'pull_number']]  # Features
# y = df['category']  # Target variable

# # Standardize the features
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)

# # Initialize Random Forest classifier
# model = RandomForestClassifier(random_state=42)

# # Define parameter grid for grid search
# param_grid = {
#     'n_estimators': [50, 100, 150],
#     'max_depth': [None, 5, 10],
#     'min_samples_split': [2, 5, 10],
#     'min_samples_leaf': [1, 2, 4]
# }

# # Split data into train and test sets
# X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# # Perform grid search
# grid_search = GridSearchCV(model, param_grid, cv=5)
# grid_search.fit(X_train, y_train)

# # Get the best parameters
# best_params = grid_search.best_params_

# # Train Random Forest model on the full dataset with the best parameters
# best_model = RandomForestClassifier(random_state=42, **best_params)
# best_model.fit(X_scaled, y)

# # Make predictions on the test set
# y_pred = best_model.predict(X_test)

# # Compute classification report
# classification_rep = classification_report(y_test, y_pred)

# # Display classification report
# print("Classification Report:")
# print(classification_rep)

# # Display the best parameters
# print("Best Parameters:", best_params)

import sqlite3
import json

# Read the JSON file
with open('output_data_barai.json', 'r') as f:
    data = json.load(f)

# Connect to SQLite3 database
conn = sqlite3.connect('github_data_all.db')
cursor = conn.cursor()

# Create a table to store the data
cursor.execute('''CREATE TABLE IF NOT EXISTS all_candidates (
                    username TEXT,
                    email TEXT,
                    followers INTEGER,
                    number_of_repos INTEGER,
                    stars INTEGER,
                    forks INTEGER,
                    pull_number INTEGER
                )''')

# Insert data into the table
for candidate in data:
    username = candidate.get('username')
    email = candidate.get('email')
    followers = candidate.get('followers')
    number_of_repos = candidate.get('number_of_repos')
    stars = candidate.get('stars')
    forks = candidate.get('forks')
    pull_number = candidate.get('pull_number')

    cursor.execute('''INSERT INTO all_candidates 
                      (username, email, followers, number_of_repos, stars, forks, pull_number) 
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                   (username, email, followers, number_of_repos, stars, forks, pull_number))

# Commit changes and close connection
conn.commit()
conn.close()

print("Data transfer completed successfully.")

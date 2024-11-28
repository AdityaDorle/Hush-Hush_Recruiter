import requests
import time
import pandas as pd
import sqlite3

def fetch_users_data(order='desc', sort='reputation', site='stackoverflow', page_size=100, min_pages=50):
    """
    Function to fetch user data from Stack Exchange API.
    """
    api_url = "https://api.stackexchange.com/2.3/users"

    users_data = []
    page = 1

    while len(users_data) < min_pages * page_size:
        params = {
            'order': order,
            'sort': sort,
            'site': site,
            'page': page,
            'pagesize': page_size
        }

        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            data = response.json().get('items', [])
            if not data:
                break
            users_data.extend(data)
            page += 1
        elif response.status_code == 400 and "backoff" in response.json():
            backoff_duration = response.json()["backoff"] + 5  # Add some extra time to backoff duration
            print(f"Received backoff parameter. Waiting for {backoff_duration} seconds...")
            time.sleep(backoff_duration)
        else:
            print(f"Error fetching data from Stack Exchange API: {response.status_code} - {response.text}")
            break

    return users_data

def create_and_populate_db(data_points, db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Create a table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        display_name TEXT,
                        reputation INTEGER,
                        gold_badges INTEGER,
                        silver_badges INTEGER
                    )''')

    # Insert data into the table
    for user_data in data_points:
        cursor.execute('''INSERT INTO users (user_id, display_name, reputation, gold_badges, silver_badges)
                          VALUES (?, ?, ?, ?, ?)''',
                       (user_data['user_id'], user_data['display_name'], user_data['reputation'],
                        user_data['gold_badges'], user_data['silver_badges']))

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Fetch user data (fetching data for at least 50 pages)
users_data = fetch_users_data(order='desc', sort='reputation', site='stackoverflow', min_pages=50)

# Extract relevant data points
data_points = []
for user in users_data:
    user_data = {
        'user_id': user['user_id'],
        'display_name': user['display_name'],
        'reputation': user['reputation'],
        'gold_badges': user['badge_counts']['gold'],
        'silver_badges': user['badge_counts']['silver']
    }
    data_points.append(user_data)

# Create and populate the SQLite database
create_and_populate_db(data_points, 'stackoverflow_users_database_for_test.db')

print("Data inserted into SQLite database successfully.")

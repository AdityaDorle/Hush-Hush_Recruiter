import requests
import time
import json

class GitHubDataFetcher:
    def __init__(self):
        self.headers = {
            # credentials removed for security purpose
        }
        self.retrieved_data = []

    def fetch_users(self):
        try:
            for i in range(0, 1000, 100):
                response = requests.get("https://api.github.com/users", params={'per_page': 100, 'since': i}, headers=self.headers)
                response.raise_for_status()
                users = response.json()
                for user in users:
                    self.retrieved_data.append(user['login'])
                time.sleep(1)  # Adding a delay to respect rate limits
        except requests.exceptions.RequestException as e:
            print(f"Error fetching users: {e}")

    def fetch_user_data(self, username):
        try:
            response = requests.get(f'https://api.github.com/users/{username}', headers=self.headers)
            time.sleep(1)  # Adding a delay to respect rate limits
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for user {username}: {e}")
            return None

    def fetch_user_repos(self, username):
        try:
            response = requests.get(f"https://api.github.com/users/{username}/repos", headers=self.headers)
            time.sleep(1)  # Adding a delay to respect rate limits
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repos for user {username}: {e}")
            return []

    def process_user_data(self, user_data, repos):
        languages = set()
        for repo in repos:
            if repo["language"]:
                languages.add(repo["language"])

        return {
            "username": user_data["login"],
            "email": user_data.get("email", "N/A"),
            "followers": user_data.get("followers", "N/A"),
            "number_of_repos": user_data.get("public_repos", "N/A"),
            "stars": sum([d["stargazers_count"] for d in repos]),
            "forks": sum([r['forks'] for r in repos]),
            "pull_number": len([r for r in repos if 'permissions' in r and 'push' in r['permissions']]),
        }

    def fetch_and_process_users_data(self):
        self.fetch_users()
        users_full_data = []

        for username in self.retrieved_data:
            user_data = self.fetch_user_data(username)
            if user_data:
                repos = self.fetch_user_repos(username)
                user_full_data = self.process_user_data(user_data, repos)
                users_full_data.append(user_full_data)

        return users_full_data

def main():
    github_fetcher = GitHubDataFetcher()
    users_data = github_fetcher.fetch_and_process_users_data()

    with open('output_data_barai_test.json', 'w') as output_file:
        json.dump(users_data, output_file, indent=4)

if __name__ == "__main__":
    main()

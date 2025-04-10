import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

gitlab_domain = 'https://YOU_DOMAIN'
personal_access_token = 'YOU_TOKEN'

headers = {
    'Private-Token': personal_access_token
}

def get_all_projects():
    page = 1
    projects = []
    while True:
        print(f"Fetching page {page} of projects...")
        response = requests.get(f'{gitlab_domain}/api/v4/projects', headers=headers, params={'page': page, 'per_page': 100}, verify=False)
        print(f"Response status code: {response.status_code}")
        
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            break
        
        data = response.json()
        if not data:
            print("No more projects to fetch.")
            break
        projects.extend(data)
        page += 1
    
    print(f"Total projects fetched: {len(projects)}")
    return projects

def main():
    try:
        projects = get_all_projects()
        repositories_dict = {project['name']: project['http_url_to_repo'] for project in projects}
        
        with open('repositories.json', 'w') as json_file:
            json.dump(repositories_dict, json_file, indent=4)
        
        print("Repository data has been written to repositories.json")
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")

if __name__ == "__main__":
    main()

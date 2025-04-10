import os
import json
import subprocess
import shutil
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

def run_command(command):
    logging.info(f"Executing: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        logging.debug(f"Command output: {result.stdout}")
        sys.stdout.flush()  
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed with error: {e.stderr}")
        sys.stdout.flush()  
        return None

def main():
    token = "YOU_TOKEN"
    gitlab_domain = "DOMAIN_NAME_WITOUT_HTTPS://"
    
    logging.info("Reading repositories from 'repositories.json'...")
    sys.stdout.flush() 
    with open('repositories.json', 'r') as file:
        repositories = json.load(file)
    logging.info(f"Found {len(repositories)} repositories to process.")
    sys.stdout.flush()

    for project_name, repo_url in repositories.items():
        logging.info(f"Processing repository: {project_name} ({repo_url})")
        sys.stdout.flush()

        repo_url_with_auth = repo_url.replace(f"https://{gitlab_domain}/", f"https://oauth2:{token}@{gitlab_domain}/")

        clone_dir = f"./{project_name}"
        logging.info(f"Cloning repository {repo_url_with_auth} into {clone_dir} with --depth 1...")
        sys.stdout.flush()
        clone_command = f'git clone --depth 1 {repo_url_with_auth} "{clone_dir}"'
        if run_command(clone_command) is None:
            logging.warning(f"Skipping repository {project_name} due to clone failure.")
            sys.stdout.flush()
            continue

        logging.info(f"Running CLOC on {clone_dir}...")
        sys.stdout.flush()
        cloc_command = f'cloc "{clone_dir}" --json'
        cloc_output = run_command(cloc_command)
        if cloc_output is not None:
            cloc_json_path = f"{project_name}_cloc.json"
            with open(cloc_json_path, 'w') as cloc_file:
                cloc_file.write(cloc_output)
            logging.info(f"CLOC data saved to {cloc_json_path}")
            sys.stdout.flush()
        else:
            logging.error(f"Failed to run CLOC on {clone_dir}")
            sys.stdout.flush()

        logging.info(f"Deleting directory {clone_dir}...")
        shutil.rmtree(clone_dir)
        logging.info(f"Directory {clone_dir} deleted.")
        sys.stdout.flush()

    logging.info("Processing completed for all repositories.")
    sys.stdout.flush()

if __name__ == "__main__":
    main()

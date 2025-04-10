import subprocess
import os

class Colors:
    HEADER = '\033[95m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def run_script(script_name, description):
    print(f"{Colors.HEADER}{Colors.BOLD}Running {script_name}...{Colors.ENDC}")
    print(f"{Colors.OKCYAN}Task: {description}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}" + "="*40 + f"{Colors.ENDC}")

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    process = subprocess.Popen(
        ['python3', script_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True,
        env=env
    )

    for line in iter(process.stdout.readline, ''):
        print(line, end='')

    process.stdout.close()
    return_code = process.wait()

    if return_code != 0:
        print(f"{Colors.FAIL}Error running {script_name}.{Colors.ENDC}")
        for line in iter(process.stderr.readline, ''):
            print(line, end='')
    else:
        print(f"{Colors.OKGREEN}{script_name} completed successfully.{Colors.ENDC}")

    print(f"{Colors.OKCYAN}" + "="*40 + f"{Colors.ENDC}\n")

if __name__ == "__main__":
    script_tasks = {
        'get_repos.py': 'Collect GitLab projects',
        'scrape_repos.py': 'Clone projects, get LOC',
        'make_csv.py': 'Make CSV'
    }

    for script, description in script_tasks.items():
        run_script(script, description)

    print(f"{Colors.OKGREEN}{Colors.BOLD}All scripts have been executed successfully.{Colors.ENDC}")
    print(f"Results in : {Colors.OKCYAN}total_gitlab_cloc.csv{Colors.ENDC}")

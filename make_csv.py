import os
import json
import csv

def process_cloc_files(directory):
    data = []

    for filename in os.listdir(directory):
        if filename.endswith("_cloc.json"):
            print(f"Processing file: {filename}")
            filepath = os.path.join(directory, filename)
            
            project_name = filename[:-10]

            with open(filepath, 'r') as file:
                try:
                    cloc_data = json.load(file)
                except json.JSONDecodeError as e:
                    print(f"Failed to decode JSON from {filename}: {e}")
                    continue

            project_data = {'Project': project_name}
            for language, metrics in cloc_data.items():
                if language not in ["header", "SUM"]:
                    project_data[language] = metrics.get("code", 0)
            
            project_data['Total'] = cloc_data.get('SUM', {}).get('code', 0)
            
            data.append(project_data)

    return data

def save_to_csv(data, output_file):
    language_totals = {}
    for project in data:
        for language, code_lines in project.items():
            if language not in ["Project", "Total"]:
                language_totals[language] = language_totals.get(language, 0) + code_lines

    sorted_languages = sorted(language_totals, key=language_totals.get, reverse=True)
    fieldnames = ['Project', 'Total'] + sorted_languages
    
    total_row = {'Project': 'TOTAL-ALL-CODE'}
    total_row['Total'] = sum(project['Total'] for project in data if 'Total' in project)
    for language in sorted_languages:
        total_row[language] = language_totals[language]

    sorted_data = sorted(data, key=lambda x: x.get('Total', 0), reverse=True)

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        writer.writerow(total_row)
        
        for project in sorted_data:
            writer.writerow(project)

def main():
    directory = '.'
    
    output_file = 'total_gitlab_cloc.csv'
    
    data = process_cloc_files(directory)
    save_to_csv(data, output_file)
    
    total_code_lines = sum(project['Total'] for project in data if 'Total' in project)
    print(f"Total lines of code across all projects: {total_code_lines}")

if __name__ == "__main__":
    main()

import csv
import json
import os

# Path to the CSV file
csv_file_path = 'codeforces_problems_with_statements.csv'
# Directory where the JSON files will be saved
json_output_directory = 'json_problems/'

# Create the directory if it doesn't exist
os.makedirs(json_output_directory, exist_ok=True)

# Function to process the CSV file and create individual JSON files
def process_csv_to_json(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            # Clean up the statement: replace newlines with spaces and escape backslashes
            cleaned_statement = row["Statement"].replace("\n", " ").replace("\\", "\\\\")
            
            # Create the JSON structure for each row
            json_entry = {
                "uid": row["Problem ID"],
                "url": row["Problem URL"],
                "tags": row["Tags"].split(',') if row["Tags"] else [],
                "title": row["Problem ID"],
                "statement": cleaned_statement,
                "source": "CF",  # Assuming CF stands for Codeforces
                "vjudge": False
            }
            
            # Define the JSON file path, using the "Problem ID" as the filename
            json_file_path = os.path.join(json_output_directory, f'{row["Problem ID"]}.json')
            
            # Write the JSON data to the file
            with open(json_file_path, mode='w', encoding='utf-8') as json_file:
                json.dump(json_entry, json_file, indent=4, ensure_ascii=False)

# Run the function to process the CSV and generate the JSON files
process_csv_to_json(csv_file_path)

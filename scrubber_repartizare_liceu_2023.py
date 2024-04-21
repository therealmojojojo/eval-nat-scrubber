import requests
import csv

# URL from which to fetch data
url = "http://static.admitere.edu.ro/2023/repartizare/B/data/candidate.json?_=1713708673231"

# Mapping from JSON keys to CSV headers
header_mapping = {
    'n': 'Codul candidatului',
    'jp': 'Județul de proveniență',
    's': 'Școala de proveniență',
    'madm': 'Media de admitere',
    'mev': 'Media EN',
    'nro': 'Nota limba română',
    'nmate': 'Nota la matematică',
    'lm': 'Limba maternă',
    'nlm': 'Nota limba maternă',
    'mabs': 'Media de absolvire',
    'h': 'Liceul în care a fost repartizat',
    'sp': 'Specializarea la care a fost repartizat'
}

# Send HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse JSON data

    # Determine the file name for the CSV
    csv_file_name = 'candidates.csv'

    # Open a new CSV file
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
        # Create a CSV writer object
        csv_writer = csv.writer(file)

        # Writing the headers based on mapping
        csv_writer.writerow([header_mapping[key] for key in sorted(header_mapping.keys())])

        # Write data rows assuming the JSON data keys correspond to the mapped keys
        for item in data:
            csv_writer.writerow([item.get(key, '') for key in sorted(header_mapping.keys())])

    print("Data successfully written to", csv_file_name)
else:
    print("Failed to retrieve data. Status code:", response.status_code)



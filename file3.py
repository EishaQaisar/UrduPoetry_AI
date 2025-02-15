import os
import csv
csv_directory = "urdu_poetry_categories"
merged_csv_file = "merged_poetry.csv"

csv_files = [file for file in os.listdir(csv_directory) if file.endswith(".csv")]

merged_data = []
serial_number = 1

for csv_file in csv_files:
    csv_path = os.path.join(csv_directory, csv_file)
    
    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        
        for row in reader:
            if len(row) == 3:  # Ensure row has Serial No., Category, Poetry
                merged_data.append([serial_number, row[1], row[2]])
                serial_number += 1  # Increment serial number

with open(merged_csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Serial No.", "Category", "Poetry"])
    writer.writerows(merged_data) 
print(f"✅ Merged {len(csv_files)} files into '{merged_csv_file}' successfully!")

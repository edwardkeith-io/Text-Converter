import pandas as pd
import re
from rapidfuzz import fuzz, process
import os
from datetime import datetime

# Configuration: Define static headers and fuzzy matchable headers
static_headers = {
    "Department": "Department:",
    "Test Code": "Test Code:",
    "Test Notes": "Test Notes:",
    "Measurement Range": "Measurement Range - ",
    "Report Range": "Report Range - ",
    "Turnaround Time": "Turnaround Time:",
    "Preferred Specimen Type": "Preferred specimen Type:",
    "Specimen Type": "Specimen Type:",
    "Sample Receptacle/Top Colour": "Sample Receptacle/Top Colour:",
    "Colour": "Colour:",
    "Ideal Sample Volume": "Ideal Sample Volume:",
    "Clinical Information": "Clinical Information:",
    "Method of Testing": "Method of Testing:",
}

fuzzy_headers = ["Note", "Additional Notes", "Laboratory Notes"]

# Initialize storage
data = []
incomplete_records = []
current_row = {}

# File paths
file_path = r"C:\Users\edwar\Downloads\SVSWebTests.txt"
output_file = r"C:\Users\edwar\Downloads\SVSWebTests_Tabulated.csv"
log_file = r"C:\Users\edwar\Downloads\Incomplete_Log.txt"

# Ensure output directory exists
output_dir = os.path.dirname(output_file)
os.makedirs(output_dir, exist_ok=True)

# Load file content
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
except FileNotFoundError:
    print(f"ERROR: File not found at {file_path}")
    exit(1)

# Check for empty file
if not lines:
    print(f"ERROR: The file at {file_path} is empty.")
    exit(1)

# Extract bullet points
def extract_bullet_points(line_iter):
    subfields = {}
    for line_number, subline in line_iter:
        subline = subline.strip()
        if subline.startswith("*"):
            key, _, value = subline[1:].partition(":")
            subfields[key.strip()] = value.strip()
        else:
            return subfields, (line_number, subline)
    return subfields, None

# Parse lines
line_iter = iter(enumerate(lines, 1))
for line_number, line in line_iter:
    line = line.strip()
    if not line:
        continue

    matched = False

    # Static headers
    for column_name, keyword in static_headers.items():
        if line.startswith(keyword):
            current_row[column_name] = line[len(keyword):].strip()
            subfields, last_line_tuple = extract_bullet_points(line_iter)
            current_row.update(subfields)
            matched = True
            break

    if matched:
        continue

    # Fuzzy headers
    for header in fuzzy_headers:
        if fuzz.partial_ratio(header.lower(), line.lower()) > 80:
            current_row[header] = line[len(header):].strip()
            subfields, last_line_tuple = extract_bullet_points(line_iter)
            current_row.update(subfields)
            matched = True
            break

    if not matched:
        previous_key = list(current_row.keys())[-1] if current_row else None
        if previous_key:
            current_row[previous_key] += " " + line
        else:
            print(f"Warning: Multiline data without a preceding header at line {line_number}.")

    # Finalize row
    if "Method of Testing" in current_row:
        for header in static_headers:
            if header not in current_row:
                current_row[header] = "N/A"
        for header in fuzzy_headers:
            if header not in current_row:
                current_row[header] = "N/A"
        data.append(current_row)
        current_row = {}
    else:
        print(f"Warning: Missing 'Method of Testing' for record starting at line {line_number}.")

# Log incomplete records
if current_row:
    incomplete_records.append({"line_number": line_number, **current_row})

# Save data
if data:
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Tabulated data saved to: {output_file}")
else:
    print("ERROR: No valid records found to save.")

# Save logs
if incomplete_records:
    with open(log_file, 'w') as log:
        for record in incomplete_records:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log.write(f"{timestamp} | Line {record['line_number']}: {record}\n")
    print(f"Log of incomplete records saved to: {log_file}")
else:
    print("No incomplete records to log.")

# Summary
print(f"Total records processed: {len(data)}")
print(f"Incomplete records logged: {len(incomplete_records)}")
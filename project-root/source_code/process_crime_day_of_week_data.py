import csv
from pathlib import Path
from datetime import datetime

# THIS SCRIPT'S DIRECTORY
script_dir = Path(__file__).resolve().parent

# GO UP ONE LEVEL (project-root)
project_root = script_dir.parent

input_file  = project_root + "data_sets" + "raw_snapshots" + "Manhattan_Crimes_2023.csv"
output_file = project_root + "data_sets" + "cleaned_data" + "crime_reports_by_weekday_2023.csv"

weekday_counts = {
    "Monday": 0,
    "Tuesday": 0,
    "Wednesday": 0,
    "Thursday": 0,
    "Friday": 0,
    "Saturday": 0,
    "Sunday": 0
}

with open(input_file, "r", newline="", encoding="utf-8") as file_in: 
    reader = csv.reader(file_in)
    header = next(reader)
    date_index = header.index("Date")
    for row in reader:
        date_str = row[date_index]
        if not date_str:
            continue
        try:
            crime_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            try:
                crime_date = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                continue
        weekday_name = crime_date.strftime("%A") # %A extracts weekday spelled out
        weekday_counts[weekday_name] += 1

with open(output_file, "w", newline="", encoding="utf-8") as file_out:
    writer = csv.writer(file_out)
    writer.writerow(["DayOfWeek", "CrimeCount"])
    for day in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]:
        writer.writerow([day, weekday_counts[day]])
        
print("Done! Wrote weekday crime counts to:", output_file)

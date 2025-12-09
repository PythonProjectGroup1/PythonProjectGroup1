import csv
import os
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

crime_file = os.path.join(project_root, "data_sets", "cleaned_data", "crime_reports_by_weekday_2023.csv")
weather_file = os.path.join(project_root, "data_sets", "raw_snapshots", "manhattan_weather_2023.csv")
output_file = os.path.join(project_root, "data_sets", "combined_data", "crime_weather_by_weekday_2023.csv")

os.makedirs(os.path.dirname(output_file), exist_ok=True)

crime_counts = {}
with open(crime_file, "r", newline="", encoding="utf-8") as f_crime:
    reader = csv.reader(f_crime)
    header = next(reader)  # ["DayOfWeek", "CrimeCount"]

    day_index = header.index("DayOfWeek")
    count_index = header.index("CrimeCount")

    for row in reader:
        day = row[day_index]
        try:
            count = int(row[count_index])
        except ValueError:
            count = 0
        crime_counts[day] = count

weekday_weather = {
    "Monday":    {"temp_sum": 0.0, "daylight_sum": 0.0, "precip_sum": 0.0, "count": 0},
    "Tuesday":   {"temp_sum": 0.0, "daylight_sum": 0.0, "precip_sum": 0.0, "count": 0},
    "Wednesday": {"temp_sum": 0.0, "daylight_sum": 0.0, "precip_sum": 0.0, "count": 0},
    "Thursday":  {"temp_sum": 0.0, "daylight_sum": 0.0, "precip_sum": 0.0, "count": 0},
    "Friday":    {"temp_sum": 0.0, "daylight_sum": 0.0, "precip_sum": 0.0, "count": 0},
    "Saturday":  {"temp_sum": 0.0, "daylight_sum": 0.0, "precip_sum": 0.0, "count": 0},
    "Sunday":    {"temp_sum": 0.0, "daylight_sum": 0.0, "precip_sum": 0.0, "count": 0},
}

with open(weather_file, "r", newline="", encoding="utf-8") as f_weather:
    reader = csv.reader(f_weather)
    header = next(reader)  # ["date","apparent_temperature_max","daylight_duration","precipitation_hours"]

    date_idx = header.index("date")
    temp_idx = header.index("apparent_temperature_max")
    daylight_idx = header.index("daylight_duration")
    precip_idx = header.index("precipitation_hours")

    for row in reader:
        if not row:
            continue

        date_str = row[date_idx]
        if not date_str:
            continue

        date_part = date_str.split(" ")[0]

        try:
            dt = datetime.strptime(date_part, "%Y-%m-%d")
        except ValueError:
            continue

        weekday_name = dt.strftime("%A")

        if weekday_name not in weekday_weather:
            continue

        try:
            temp = float(row[temp_idx])
        except ValueError:
            temp = 0.0

        try:
            daylight = float(row[daylight_idx])
        except ValueError:
            daylight = 0.0

        try:
            precip = float(row[precip_idx])
        except ValueError:
            precip = 0.0

        weekday_weather[weekday_name]["temp_sum"] += temp
        weekday_weather[weekday_name]["daylight_sum"] += daylight
        weekday_weather[weekday_name]["precip_sum"] += precip
        weekday_weather[weekday_name]["count"] += 1

with open(output_file, "w", newline="", encoding="utf-8") as f_out:
    writer = csv.writer(f_out)

    writer.writerow([
        "DayOfWeek",
        "CrimeCount",
        "AverageApparentTempMax",
        "AverageDaylightDuration",
        "AveragePrecipitationHours",
    ])

    ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for day in ordered_days:
        crime_count = crime_counts.get(day, 0)
        stats = weekday_weather[day]
        if stats["count"] > 0:
            avg_temp = stats["temp_sum"] / stats["count"]
            avg_daylight = stats["daylight_sum"] / stats["count"]
            avg_precip = stats["precip_sum"] / stats["count"]
        else:
            avg_temp = 0.0
            avg_daylight = 0.0
            avg_precip = 0.0

        writer.writerow([
            day,
            crime_count,
            round(avg_temp, 3),
            round(avg_daylight, 3),
            round(avg_precip, 3),
        ])

print("Done! Wrote combined crime + weather data to:", output_file)
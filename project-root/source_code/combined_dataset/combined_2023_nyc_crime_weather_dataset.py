import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sodapy import Socrata
import os

crime_file_name = "crime_cleaned.csv"
print("Loading crime data from:", crime_file_name)
df_crime_clean = pd.read_csv(crime_file_name)

weather_file_name = "weather_cleaned.csv"
print("Loading weather data from:", weather_file_name)
df_weather_clean = pd.read_csv(weather_file_name)

print("Merging data on 'Date'...")
df_merged = pd.merge(df_crime_clean, df_weather_clean, on="Date", how="inner")

print("Merged Data contains", len(df_merged), "rows.")
print("Here are the first 5 rows of the merged data:")
print(df_merged.head())

output_file_name = os.path.join("..", "..", "data_sets", "combined_data", "combined_2023_crime_weather_data.json") # the two  ".." causes path to go up two levels  
print("Saving merged data to JSON at:", output_file_name)
df_merged.to_json(output_file_name, orient="records")

print("JSON file created.")

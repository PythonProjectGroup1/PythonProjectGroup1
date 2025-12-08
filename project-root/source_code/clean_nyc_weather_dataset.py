from pathlib import Path
import pandas as pd
from paths import NYC_WEATHER_CSV, CLEANED_NYC_WEATHER_CSV
from constants import DAYLIGHT_HOUR_DIVISOR, DECIMAL_PLACES
from helper_functions import fetch_csv

def normalize_date_column(df_weather: pd.DataFrame):
    #  Converts 'date' to standard panda date_times.
    #  Renames 'date' column to 'Date' to standardize columns across csv files
    df_weather['date'] = pd.to_datetime(df_weather['date'], errors='coerce', utc=True)
    df_weather['date'] = df_weather['date'].dt.date
    df_weather.rename(columns={'date': 'Date'}, inplace=True)

def round_temperature_values(df_weather: pd.DataFrame):
    # Rounds 'apparent_temperature_max' to the value of DECIMAL_PLACES

    df_weather['apparent_temperature_max'] = (
        df_weather['apparent_temperature_max'].round(DECIMAL_PLACES)
    )

def convert_daylight_to_hours(df_weather: pd.DataFrame):
    # Converts 'daylight_duration' from seconds to hours
    # Rounds to the value of DECIMAL_PLACES
    # Renames column to 'daylight_hours'

    df_weather['daylight_duration'] = (
        df_weather['daylight_duration'] / DAYLIGHT_HOUR_DIVISOR
    ).round(DECIMAL_PLACES)

    df_weather.rename(
        columns={'daylight_duration': 'daylight_hours'}, 
        inplace=True
    )    
    
def export_clean_weather_csv(df_weather: pd.DataFrame) -> None:
    df_weather.to_csv(CLEANED_NYC_WEATHER_CSV, index=False)
    print(f"Saved cleaned weather data to: {CLEANED_NYC_WEATHER_CSV}")
    print(df_weather.head())

def main():
    df_weather = fetch_csv(path=NYC_WEATHER_CSV)
    normalize_date_column(df_weather)
    round_temperature_values(df_weather)
    convert_daylight_to_hours(df_weather)
    export_clean_weather_csv(df_weather)

if __name__ == "__main__":
    main()
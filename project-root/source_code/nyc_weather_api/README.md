# Weather Data API

This directory contains modules used to process historical weather data retrieved from an external weather API.

- **fetch_weather_api.py**  
  Retrieves historical weather data and stores it as a raw snapshot.

- **clean_weather_dataset.py**  
  Cleans the raw snapshot by standardizing column names, fixing formats and handling missing values. Edits the cleaned dataset by grouping date and location to produce a merge-ready table compatible with nyc crime data.
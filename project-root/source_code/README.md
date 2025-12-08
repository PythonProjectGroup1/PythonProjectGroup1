# Source Code Directory

This folder contains all of the Python files used to fetch, clean, prepare and combine data.

- **api_config/**  
  YAML files containing API endpoints, authentication settings, and query parameters.

## NYC Crime API
  To run the script make sure `sodapy` and `pandas` and `PyYAML` are installed in your environment.
  pip install sodapy
  pip install PyYAML
  pip install pandas
    
  Files for retrieving and cleaning NYC crime data.

## Weather Data API
 To run the script make sure `openmeteo-requests`, `requests-cache`,`PyYAML`, `retry-requests`, `numpy` and `pandas` are installed in your environment.
  pip install openmeteo-requests
  pip install PyYAML
  pip install requests-cache retry-requests numpy pandas

- **fetch_weather_api.py**  
  Retrieves historical weather data and stores it as a raw snapshot.
 
- **clean_weather_dataset.py**  
  Cleans the raw snapshot by standardizing column names, fixing formats and handling missing values. Edits the cleaned dataset by grouping date and location to produce a merge-ready table compatible with nyc crime data.

- **data_summary_tools/**  
  Functions responsible for generating summaries of our data (temperatures with the highest crime, hours / days when crime is more likely, etc...).

- **combined_dataset/** 
    Files for combining the crime and weather datasets
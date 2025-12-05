# NYC Crime Data API

This directory contains all functions responsible for transforming NYC crime data from raw API output to a merge-ready dataset.

- **fetch_from_nyc_api.py**  
  Retrieves historical NYC crime data from the NYC Open Data API and saves a raw snapshot locally.

- **clean_nyc_dataset.py**  
  Cleans the raw snapshot by standardizing column names, fixing formats and handling missing values. Edits the cleaned dataset by grouping date and location to produce a merge-ready table compatible with weather data.
  

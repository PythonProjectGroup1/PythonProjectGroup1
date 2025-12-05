# Datasets Directory

This directory contains all datasets used or produced for the project.  
Each dataset represents a different stage of our data analysis.

## Structure

- **raw_snapshots/**  
  Contains unmodified API responses saved locally.

- **cleaned_data/**  
  Contains datasets that have been cleaned and standardized. Missing values, and structural issues should be corrected at this point. Crime and weather data should be formatted by shared keys (e.g., date, borough, zipcode, etc...) so they can be safely combined.

- **combined_data/**  
  Contains a merged crime + weather dataset. 

## Notes
- Raw files are never altered
- Cleaned and combined data files are created by scripts in `source_code/`

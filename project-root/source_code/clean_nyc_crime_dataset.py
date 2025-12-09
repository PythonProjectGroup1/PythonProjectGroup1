from pathlib import Path
import pandas as pd
from paths import NYC_CRIME_CSV, CLEANED_NYC_CRIME_CSV
from constants import DAYLIGHT_HOUR_DIVISOR, DECIMAL_PLACES, PUBLIC_ORDER_CRIMES, VIOLENT_CRIMES, PROPERTY_CRIMES, PROPERTY_KEYWORDS, VIOLENT_KEYWORDS
from helper_functions import fetch_csv

def standardize_date_column(df_crime: pd.DataFrame):
    #  Converts 'date' to standard panda date_times.
    #  Renames 'date' column to 'Date' to standardize columns across csv files
    df_crime.rename(columns={'cmplnt_fr_dt': 'Date'}, inplace=True)
    df_crime['Date'] = pd.to_datetime(df_crime['Date'], errors='coerce', utc=True)
    df_crime['Date'] = df_crime['Date'].dt.date
    df_crime.sort_values(by='Date', inplace=True)

def standardize_crime_column(df_crime: pd.DataFrame):
    # Renames 'ofns_desc' column to 'crime_type'
    # Condenses crime descriptions (63) into 3 clear categories 
    df_crime.rename(columns={"ofns_desc": "crime_type"},inplace=True)
    group_crime_categories(df_crime)

def classify_crime(crime: str) -> str:
    if crime in PUBLIC_ORDER_CRIMES:
        return "public_order"
    elif crime in VIOLENT_CRIMES:
        return "violent"
    elif crime in PROPERTY_CRIMES:
        return "property"
    else:
        return "public_order"

def classify_ambiguous_crime(crime):
    if crime in PROPERTY_KEYWORDS:
        return "property"
    elif crime in VIOLENT_KEYWORDS:
        return "violent"
    else: 
        return "public_order"
    
def assign_crime_group(row):
    crime = row["crime_type"]
    official_crimes = VIOLENT_CRIMES | PROPERTY_CRIMES | PUBLIC_ORDER_CRIMES
    if crime in official_crimes:
        return classify_crime(crime)

    # If the crime is ambiguous ('MISCELLANEOUS PENAL LAW' for example) use pd_desc (internal police descriptions):
    return classify_ambiguous_crime(row["pd_desc"])

def drop_unused_columns(df_crime: pd.DataFrame, column_names:list):
    for column in column_names:
        try:
            df_crime.drop(columns=column,inplace=True)
        except:
            continue

def group_crime_categories(df_crime: pd.DataFrame):
    df_crime["crime_group"] = df_crime.apply(assign_crime_group, axis=1)

def group_crimes_by_date(df_crime: pd.DataFrame) -> pd.DataFrame:
    # Group totals by crime_group (property / violent / public_order) ---
    totals = (
        df_crime
        .groupby(['Date', 'crime_group'])
        .size()
        .unstack('crime_group', fill_value=0)
    )

    totals = totals.rename(columns={
        'property': 'property_crimes',
        'violent': 'violent_crimes',
        'public_order': 'public_order_crimes'
    })

    totals['total_crimes'] = (
        totals['property_crimes']
        + totals['violent_crimes']
        + totals['public_order_crimes']
    )

    # --- 2. Per-crime counts (crime_type columns) ---
    crime_counts = (
        df_crime
        .groupby(['Date', 'crime_type'])
        .size()
        .unstack('crime_type', fill_value=0)
    )

    combined = totals.join(crime_counts, how='left')

    combined = combined.reset_index()

    total_cols = [
        'Date',
        'property_crimes',
        'violent_crimes',
        'public_order_crimes',
        'total_crimes'
    ]
    crime_type_cols = []

    for column_name in combined.columns:
     if column_name not in total_cols:
        crime_type_cols.append(column_name)

    combined = combined[total_cols + crime_type_cols]
    # Removes redundant borough column
    drop_unused_columns(combined,['boro_nm','(null)'])
    return combined

def export_as_csv(df_crime: pd.DataFrame):
    df_crime.to_csv(CLEANED_NYC_CRIME_CSV, index=False)
    print(f"Saved cleaned crime data to: {CLEANED_NYC_CRIME_CSV}")
    print(df_crime.head())


def main():
    # Grabs raw csv file from RAW_SNAPSHOTS
    df_crime = fetch_csv(NYC_CRIME_CSV)
    # Standardizes date format 
    standardize_date_column(df_crime)
    # Merges dozens of crimes into 3 distinct categories
    standardize_crime_column(df_crime)
    export_as_csv(group_crimes_by_date(df_crime))

main()


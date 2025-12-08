import pandas as pd
from sodapy import Socrata
from helper_functions import get_secret_token, load_config
from paths import NYC_CRIME_CSV, NYC_CRIME_CONFIG

def get_secret(alias) -> str:
   # returns token stored in a git-ignored secrets file
    return get_secret_token(alias)  

def build_socrata_client(client_config: dict) -> Socrata:
    # builds socrata client using values stored in the nyc_crime yaml file

    app_token = get_secret(client_config["app_token"])
    client = Socrata(
        client_config["domain"],
        app_token,
        timeout=client_config["timeout"]
    )
    return client


def fetch_crime_results(client: Socrata, query_config: dict) -> pd.DataFrame:
    dataset_id = get_secret(query_config["dataset_id"])

    results = client.get(
        dataset_id,
        where=query_config["where"],
        select=query_config["select"],
        limit=query_config["limit"]
    )
    return pd.DataFrame.from_records(results)

def export_as_csv(df: pd.DataFrame):
    df.to_csv(NYC_CRIME_CSV, index = False)

    print(f"Success! Saved {len(df)} rows to {NYC_CRIME_CSV}.")
    print(df.head())


#df.rename(columns = {"cmplnt_fr_dt": "Date", "ofns_desc": "Crime_Name", "boro_nm": "Borough"}, inplace = True)

# Save to CSV
def main():
    config = load_config(NYC_CRIME_CONFIG)['socrata']
    client = build_socrata_client(config["client"])
    df_crime = fetch_crime_results(client, config["query"])
    export_as_csv(df_crime)

if __name__ == "__main__":
    main()
import pandas as pd
from sodapy import Socrata

app_token = "BBAWxt0lQlAFKbBQfnE8G5KJx"
client = Socrata("data.cityofnewyork.us", app_token, timeout=60)
dataset_id = "qgea-i56i"

results = client.get(
    dataset_id,
    where = "cmplnt_fr_dt between '2023-01-01T00:00:00' and '2023-12-31T23:59:59' AND boro_nm = 'MANHATTAN'",
    select = "cmplnt_fr_dt, ofns_desc, boro_nm",
    limit = 150000 
)
df = pd.DataFrame.from_records(results)

df.rename(columns = {"cmplnt_fr_dt": "Date", "ofns_desc": "Crime_Name", "boro_nm": "Borough"}, inplace = True)

# Save to CSV
df.to_csv("Manhattan_Crimes_2023.csv", index = False)

print(f"Success! Saved {len(df)} rows to 'Manhattan_Crimes_2023.csv'.")
print(df.head())
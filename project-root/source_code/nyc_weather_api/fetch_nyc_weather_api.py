from pathlib import Path
import yaml
import pandas as pd
import requests_cache
from retry_requests import retry
import openmeteo_requests
from source_code.paths import NYC_WEATHER_CONFIG, RAW_SNAPSHOTS_DIR
#from paths import NYC_WEATHER_CONFIG, RAW_SNAPSHOTS_DIR

#CONSTANTS
YAML_DIRECTORY = (Path(__file__).parent / 'api_config' / "nyc_weather_endpoints.yaml").resolve()
#print(NYC_WEATHER_CONFIG)
print(NYC_WEATHER_CONFIG)
# def load_config():
#     script_directory = Path(__file__).parent
#     config_path = script_directory.parent / "api_config" / "nyc_weather_endpoints.yaml"
#     config_path = config_path.resolve()
#     with open(config_path, "r") as file:
#         return yaml.safe_load(file)


# def create_openmeteo_client(api_config: dict) -> openmeteo_requests.Client:
#     """
#     Create an Open-Meteo client with caching and retry logic
#     using the settings from the YAML config.
#     """
#     cache_cfg = api_config["client"]["cache"]
#     retry_cfg = api_config["client"]["retry"]

#     # Cached HTTP session
#     cache_session = requests_cache.CachedSession(
#         cache_name=cache_cfg["backend"],
#         expire_after=cache_cfg["expire_after_seconds"],
#     )

#     # Wrap with retry logic
#     retry_session = retry(
#         cache_session,
#         retries=retry_cfg["retries"],
#         backoff_factor=retry_cfg["backoff_factor"],
#     )

    

#     return openmeteo_requests.Client(session=retry_session)

# def fetch_daily_weather(
#     client: openmeteo_requests.Client, api_config: dict
# ) -> pd.DataFrame:
#     """
#     Call the Open-Meteo API and return a pandas DataFrame
#     with daily variables for the configured location and date range.

#     Expected daily variables in order:
#       0: apparent_temperature_max
#       1: daylight_duration
#       2: precipitation_hours
#     """
#     url = api_config["url"]
#     params = api_config["params"]

#     # Call Open-Meteo; returns a list of response objects (one per location)
#     responses = client.weather_api(url, params=params)

#     # We expect a single location (centroid) from the config
#     response = responses[0]

#     daily = response.Daily()

#     # ORDER MUST MATCH params["daily"] IN CONFIG
#     apparent_max = daily.Variables(0).ValuesAsNumpy()
#     daylight_duration = daily.Variables(1).ValuesAsNumpy()
#     precipitation_hours = daily.Variables(2).ValuesAsNumpy()

#     # Construct date range from metadata
#     dates = pd.date_range(
#         start=pd.to_datetime(daily.Time(), unit="s", utc=True),
#         end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
#         freq=pd.Timedelta(seconds=daily.Interval()),
#         inclusive="left",
#     )

#     df = pd.DataFrame(
#         {
#             "date": dates,
#             "apparent_temperature_max": apparent_max,
#             "daylight_duration": daylight_duration,
#             "precipitation_hours": precipitation_hours,
#         }
#     )

#     # Convert UTC to configured timezone (e.g. America/New_York), if provided
#     timezone = params.get("timezone")
#     if timezone:
#         df["date"] = df["date"].dt.tz_convert(timezone)

#     return df

# def get_output_path() -> str:
#     # project-root\data_sets\raw_snapshots
#     project_root = Path(__file__).parent.parent.parent
#     output_dir = project_root / "data_sets" / "raw_snapshots" 
#     print(Path(__file__))
#     print(project_root)
#     print(output_dir)
#     return output_dir / "manhattan_weather_2023.csv"


# def main() -> None:
#     # # 1) Load configuration
#     # config = load_config()
#     # api_config = config["open_meteo"]

#     # # 2) Create Open-Meteo client
#     # client = create_openmeteo_client(api_config)

#     # # 3) Fetch daily weather into a DataFrame
#     # df = fetch_daily_weather(client, api_config)

#     # # 4) Save to CSV in project-root/data_sets/raw_snapshots
#     output_file = get_output_path()
#     # df.to_csv(output_file, index=False)

#     # print(f"Saved weather CSV to:\n{output_file}")
#     # print("\nPreview:\n", df.head())


# if __name__ == "__main__":
#     main()
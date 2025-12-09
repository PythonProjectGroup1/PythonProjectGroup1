import pandas as pd
import requests_cache
from retry_requests import retry
import openmeteo_requests
from paths import NYC_WEATHER_CONFIG, NYC_WEATHER_CSV
from helper_functions import load_config

def create_openmeteo_client(api_config: dict) -> openmeteo_requests.Client:
    # Creates an Open-Meteo client (example set up found here: https://open-meteo.com/en/docs/historical-forecast-api) that includes caching and retry logic
    # using the settings from the YAML config.
   
    cache_cfg = api_config["client"]["cache"]
    retry_cfg = api_config["client"]["retry"]

    # Cache
    cache_session = requests_cache.CachedSession(
        cache_name=cache_cfg["backend"],
        expire_after=cache_cfg["expire_after_seconds"],
    )

    # Retry
    retry_session = retry(
        cache_session,
        retries=retry_cfg["retries"],
        backoff_factor=retry_cfg["backoff_factor"],
    )

    return openmeteo_requests.Client(session=retry_session)

def fetch_daily_weather(
    client: openmeteo_requests.Client, api_config: dict
) -> pd.DataFrame:
    
    # Calls the Open-Meteo API and returns a DataFrame
    # with daily variables for the location and date range.

    # The daily variables for this project are:
    #   0: apparent_temperature_max
    #   1: daylight_duration
    #   2: precipitation_hours

    url = api_config["url"]
    params = api_config["params"]

    # Call Open-Meteo and returns a list of response objects
    responses = client.weather_api(url, params=params)

    # We're only using one location (the Central Park Observatory site) for borough-wide weather data. The max temperature difference between Central Park and Manhattan as a whole is extremely small (usually 1 or 2 degrees on average). Additionally federal, state and academic climate studies all use this station as the reference point for Manhattan
    response = responses[0]

    daily = response.Daily()

    apparent_max = daily.Variables(0).ValuesAsNumpy()
    daylight_duration = daily.Variables(1).ValuesAsNumpy()
    precipitation_hours = daily.Variables(2).ValuesAsNumpy()

    # date range
    dates = pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left",
    )

    df_weather = pd.DataFrame(
        {
            "date": dates,
            "apparent_temperature_max": apparent_max,
            "daylight_duration": daylight_duration,
            "precipitation_hours": precipitation_hours,
        }
    )

    timezone = params.get("timezone")
    if timezone:
        df_weather["date"] = df_weather["date"].dt.tz_convert(timezone)

    return df_weather

def export_weather_cvs(df_weather: pd.DataFrame):
    df_weather.to_csv(NYC_WEATHER_CSV, index=False)

    print(f"Saved weather CSV to:\n{NYC_WEATHER_CSV}")
    print("\nPreview:\n", df_weather.head())

def main():
    # Load configuration from yaml file
    config = load_config(NYC_WEATHER_CONFIG)
    api_config = config["open_meteo"]

    # Create Open-Meteo client
    client = create_openmeteo_client(api_config)

    # Fetch daily weather and convert it into a DataFrame
    df_weather = fetch_daily_weather(client, api_config)

    # Save to CSV in project-root/data_sets/raw_snapshots
    export_weather_cvs(df_weather)


if __name__ == "__main__":
    main()
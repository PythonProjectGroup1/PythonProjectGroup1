from pathlib import Path

# Directory containing the source_code folder
SOURCE_ROOT = Path(__file__).resolve().parent

# Project root (one level above source_code)
PROJECT_ROOT = SOURCE_ROOT.parent

# Config directories
API_CONFIG_DIR = SOURCE_ROOT / "api_config"
NYC_WEATHER_CONFIG = API_CONFIG_DIR / "nyc_weather_endpoints.yaml"

# Data directories
DATASETS_DIR = PROJECT_ROOT / "data_sets"
RAW_SNAPSHOTS_DIR = DATASETS_DIR / "raw_snapshots"
CLEANED_DATA_DIR = DATASETS_DIR / "cleaned_data"
# CSV
NYC_WEATHER_CSV = RAW_SNAPSHOTS_DIR / "manhattan_weather_2023.csv"
CLEANED_NYC_WEATHER_CSV = CLEANED_DATA_DIR / "cleaned_manhattan_weather_2023.csv"
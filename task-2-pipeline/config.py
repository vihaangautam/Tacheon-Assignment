# config.py
# All pipeline parameters live here. Never hardcode in logic files.

import os
from datetime import datetime, timedelta

# --- API ---
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "your_api_key_here")
NEWS_API_BASE_URL = "https://newsapi.org/v2/top-headlines"
NEWS_API_QUERY = os.getenv("NEWS_QUERY", "marketing")        # topic/brand to track
NEWS_API_LANGUAGE = os.getenv("NEWS_LANGUAGE", "en")
NEWS_API_PAGE_SIZE = int(os.getenv("NEWS_PAGE_SIZE", "100")) # max per request
NEWS_API_FROM_DATE = os.getenv(
    "NEWS_FROM_DATE",
    (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
)

# --- BigQuery ---
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-project-id")
BQ_DATASET = os.getenv("BQ_DATASET", "news_pipeline")
BQ_TABLE = os.getenv("BQ_TABLE", "articles")

# --- Pipeline ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

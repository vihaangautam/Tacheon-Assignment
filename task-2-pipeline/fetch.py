# fetch.py

import requests
import logging
from config import NEWS_API_KEY, NEWS_API_BASE_URL, NEWS_API_QUERY, NEWS_API_LANGUAGE, NEWS_API_PAGE_SIZE, NEWS_API_FROM_DATE

logger = logging.getLogger(__name__)


class FetchError(Exception):
    """Raised when the API call fails unrecoverably."""
    pass


def fetch_articles() -> list[dict]:
    """
    Fetch top headlines from NewsAPI.
    Returns a list of raw article dicts.
    Raises FetchError on unrecoverable failure.
    """
    params = {
        "apiKey": NEWS_API_KEY,
        "q": NEWS_API_QUERY,
        "language": NEWS_API_LANGUAGE,
        "pageSize": NEWS_API_PAGE_SIZE,
        "from": NEWS_API_FROM_DATE,
    }

    logger.info(f"Fetching articles | query='{NEWS_API_QUERY}' from={NEWS_API_FROM_DATE}")

    try:
        response = requests.get(NEWS_API_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise FetchError("NewsAPI request timed out after 10 seconds")
    except requests.exceptions.HTTPError as e:
        raise FetchError(f"NewsAPI returned HTTP error: {e.response.status_code} — {e.response.text}")
    except requests.exceptions.RequestException as e:
        raise FetchError(f"Unexpected request error: {str(e)}")

    data = response.json()

    if data.get("status") != "ok":
        raise FetchError(f"NewsAPI returned non-ok status: {data.get('message', 'unknown error')}")

    articles = data.get("articles", [])
    logger.info(f"Fetched {len(articles)} articles successfully")

    return articles

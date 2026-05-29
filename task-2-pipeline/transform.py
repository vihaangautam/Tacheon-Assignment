# transform.py

import logging
from datetime import datetime, timezone
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def transform_articles(raw_articles: list[dict]) -> list[dict]:
    """
    Clean and enrich raw NewsAPI article dicts.
    Returns list of flat dicts ready for BigQuery insertion.
    """
    transformed = []
    skipped = 0

    for article in raw_articles:
        try:
            row = _transform_single(article)
            transformed.append(row)
        except Exception as e:
            logger.warning(f"Skipping article due to transform error: {e} | article: {article.get('url', 'unknown')}")
            skipped += 1

    logger.info(f"Transform complete | success={len(transformed)} skipped={skipped}")
    return transformed


def _transform_single(article: dict) -> dict:
    source = article.get("source") or {}
    url = article.get("url") or ""
    title = article.get("title") or ""
    description = article.get("description")
    published_raw = article.get("publishedAt")

    # Parse published timestamp
    published_at = None
    if published_raw:
        try:
            published_at = datetime.strptime(published_raw, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        except ValueError:
            logger.warning(f"Could not parse publishedAt: {published_raw}")

    # Extract domain from URL
    source_domain = None
    if url:
        try:
            source_domain = urlparse(url).netloc.replace("www.", "")
        except Exception:
            pass

    return {
        # Core fields
        "article_url":       url or None,
        "title":             title or None,
        "description":       description or None,
        "author":            article.get("author") or None,
        "content_snippet":   (article.get("content") or "")[:500] or None,  # truncate to 500 chars
        "published_at":      published_at.isoformat() if published_at else None,

        # Flattened source
        "source_id":         source.get("id") or None,
        "source_name":       source.get("name") or None,
        "source_domain":     source_domain,

        # Derived fields (analytical value)
        "title_word_count":  len(title.split()) if title else 0,
        "has_description":   description is not None and len(description.strip()) > 0,
        "query_term":        _get_query_term(),   # tag which query produced this row

        # Pipeline metadata
        "ingested_at":       datetime.now(timezone.utc).isoformat(),
    }


def _get_query_term() -> str:
    from config import NEWS_API_QUERY
    return NEWS_API_QUERY

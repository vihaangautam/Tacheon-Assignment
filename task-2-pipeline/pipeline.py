# pipeline.py
# Entry point. Runs fetch → transform → load in sequence.

import logging
import sys
from config import LOG_LEVEL
from fetch import fetch_articles, FetchError
from transform import transform_articles
from load import load_to_bigquery

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

logger = logging.getLogger("pipeline")


def run():
    logger.info("=== Pipeline starting ===")

    # Step 1: Fetch
    try:
        raw = fetch_articles()
    except FetchError as e:
        logger.error(f"Fetch failed: {e}")
        sys.exit(1)

    if not raw:
        logger.warning("No articles returned from API — nothing to process")
        sys.exit(0)

    # Step 2: Transform
    transformed = transform_articles(raw)

    if not transformed:
        logger.warning("Transform produced no rows — nothing to load")
        sys.exit(0)

    # Step 3: Load
    load_to_bigquery(transformed)

    logger.info("=== Pipeline complete ===")


if __name__ == "__main__":
    run()

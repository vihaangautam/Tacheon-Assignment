# load.py

import logging
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from config import GCP_PROJECT_ID, BQ_DATASET, BQ_TABLE

logger = logging.getLogger(__name__)

SCHEMA = [
    bigquery.SchemaField("article_url",      "STRING"),
    bigquery.SchemaField("title",            "STRING"),
    bigquery.SchemaField("description",      "STRING"),
    bigquery.SchemaField("author",           "STRING"),
    bigquery.SchemaField("content_snippet",  "STRING"),
    bigquery.SchemaField("published_at",     "TIMESTAMP"),
    bigquery.SchemaField("source_id",        "STRING"),
    bigquery.SchemaField("source_name",      "STRING"),
    bigquery.SchemaField("source_domain",    "STRING"),
    bigquery.SchemaField("title_word_count", "INTEGER"),
    bigquery.SchemaField("has_description",  "BOOLEAN"),
    bigquery.SchemaField("query_term",       "STRING"),
    bigquery.SchemaField("ingested_at",      "TIMESTAMP"),
]


def get_or_create_table(client: bigquery.Client) -> bigquery.Table:
    dataset_ref = bigquery.DatasetReference(GCP_PROJECT_ID, BQ_DATASET)

    # Create dataset if missing
    try:
        client.get_dataset(dataset_ref)
    except NotFound:
        logger.info(f"Dataset {BQ_DATASET} not found — creating")
        client.create_dataset(bigquery.Dataset(dataset_ref))

    table_ref = dataset_ref.table(BQ_TABLE)

    # Create table if missing
    try:
        table = client.get_table(table_ref)
        logger.info(f"Table {BQ_TABLE} already exists")
    except NotFound:
        logger.info(f"Table {BQ_TABLE} not found — creating with schema")
        table = bigquery.Table(table_ref, schema=SCHEMA)
        table = client.create_table(table)

    return table


def load_to_bigquery(rows: list[dict]) -> None:
    if not rows:
        logger.warning("No rows to load — skipping BigQuery write")
        return

    client = bigquery.Client(project=GCP_PROJECT_ID)
    table = get_or_create_table(client)

    logger.info(f"Loading {len(rows)} rows into {GCP_PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}")

    errors = client.insert_rows_json(table, rows)

    if errors:
        logger.error(f"BigQuery insert errors: {errors}")
        raise RuntimeError(f"BigQuery load failed with {len(errors)} error(s)")

    logger.info(f"Successfully loaded {len(rows)} rows")

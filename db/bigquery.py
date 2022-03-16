from typing import Any, Optional
from datetime import datetime

from google.cloud import bigquery

BQ_CLIENT = bigquery.Client()

DATASET = "Shopify"


def get_last_timestamp(table: str, cursor_key: str):
    def _get(
        timeframe: tuple[Optional[str], Optional[str]]
    ) -> tuple[datetime, datetime]:
        start, end = timeframe
        if start and end:
            return tuple([datetime.strptime(i, "%Y-%m-%d") for i in (start, end)])  # type: ignore
        else:
            rows = BQ_CLIENT.query(
                f"SELECT MAX({cursor_key}) AS incre FROM {DATASET}.{table}"
            ).result()
            return (
                [row for row in rows][0]["incre"],
                datetime.utcnow(),
            )

    return _get


def load(
    name: str,
    table: str,
    schema: list[dict[str, Any]],
    id_key: str,
    cursor_key: str,
):
    def _load(data: list[dict[str, Any]]) -> int:
        if len(data) == 0:
            return 0

        output_rows = (
            BQ_CLIENT.load_table_from_json(
                data,
                f"{name}_{DATASET}.{table}",
                job_config=bigquery.LoadJobConfig(
                    create_disposition="CREATE_IF_NEEDED",
                    write_disposition="WRITE_APPEND" if id_key else "WRITE_TRUNCATE",
                    schema=schema,
                ),
            )
            .result()
            .output_rows
        )
        if id_key and cursor_key:
            _update(name, table, id_key, cursor_key)
        return output_rows

    return _load


def _update(name: str, table: str, id_key: str, cursor_key: str):
    BQ_CLIENT.query(
        f"""
    CREATE OR REPLACE TABLE {name}_{DATASET}.{table} AS
    SELECT * EXCEPT(row_num)
    FROM (
        SELECT
            *,
            ROW_NUMBER() OVER (
                PARTITION BY {id_key}
                ORDER BY {cursor_key} DESC
            ) AS row_num,
        FROM {name}_{DATASET}.{table}
    ) WHERE row_num = 1
    """
    ).result()

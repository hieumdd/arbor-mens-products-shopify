from typing import Optional, Union

from compose import compose

from shopify import shopify, shopify_repo, orders
from db.bigquery import get_last_timestamp, load

pipelines = {
    i.table: i
    for i in [
        orders.orders,
    ]
}

shops = {
    i.shop_url: i
    for i in [
        shopify.Auth("arbor-mens-products", ""),
    ]
}


def pipeline_service(
    pipeline: shopify.Pipeline,
    auth: shopify.Auth,
    start: Optional[str],
    end: Optional[str],
) -> dict[str, Union[str, int]]:
    return compose(
        lambda x: {
            "table": pipeline.table,
            "shop_url": auth.shop_url,
            "start": start,
            "end": end,
            "output_rows": x,
        },
        load(pipeline.table, pipeline.schema, pipeline.id_key, pipeline.cursor_key),
        pipeline.transform,
        shopify_repo.get(pipeline.resource, auth),
        get_last_timestamp(pipeline.table, pipeline.cursor_key),
    )((start, end))

from typing import Union, Any
from datetime import datetime

import requests

from shopify import shopify

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

API_VER = "2022-01"


def get_url(endpoint: str, shop_url: str) -> str:
    return f"https://{shop_url}.myshopify.com/admin/api/{API_VER}/{endpoint}"


def get_session(access_token: str) -> requests.Session:
    client = requests.Session()
    client.headers.update({"access_token": access_token})
    return client


def build_params(
    fields: list[str],
    timeframe: tuple[datetime, datetime],
) -> dict[str, Union[str, int]]:
    start, end = [i.strftime(TIMESTAMP_FORMAT) for i in timeframe]
    return {
        "limit": 250,
        "status": "any",
        "fields": ",".join(fields),
        "updated_at_min": start,
        "updated_at_max": end,
    }


def get(resource: shopify.Resource, auth: shopify.Auth):
    def _get(timeframe: tuple[datetime, datetime]):
        def __get(
            client: requests.Session,
            params: dict[str, Union[str, int]],
            url: str,
        ) -> list[dict[str, Any]]:
            with client.get(url, params) as r:
                res = r.json()
            data = res[resource.data_key]
            next_link = r.links.get("next")
            return (
                data + __get(client, params, next_link.get("url"))
                if next_link
                else data
            )

        with get_session(auth.access_token) as client:
            return __get(
                client,
                build_params(resource.fields, timeframe),
                get_url(resource.endpoint, auth.access_token),
            )

    return _get

from typing import Any, Union

from shopify import shopify_service


def shopify_controller(body: dict[str, Any]) -> dict[str, Union[str, int]]:
    return shopify_service.pipeline_service(
        shopify_service.pipelines[body["resource"]],
        shopify_service.shops[body["shop"]],
        body.get("start"),
        body.get("end"),
    )

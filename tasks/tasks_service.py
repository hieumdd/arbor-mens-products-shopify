from shopify import shopify_service
from tasks import cloud_tasks


def tasks_service(body: dict[str, str]):
    return {
        "tasks": cloud_tasks.create_tasks(
            [
                {
                    "resource": p,
                    "shop": s,
                    "start": body.get("start"),
                    "end": body.get("end"),
                }
                for p in shopify_service.pipelines.keys()
                for s in shopify_service.shops.keys()
            ],
            lambda x: f"{x['resource']}-{x['shop']}",
        )
    }

import pytest

from shopify import shopify_service

TIMEFRAME = [
    ("auto", (None, None)),
    ("manual", ("2022-01-01", "2022-04-01")),
]


@pytest.fixture(
    params=[i[1] for i in TIMEFRAME],
    ids=[i[0] for i in TIMEFRAME],
)
def timeframe(request):
    return request.param


@pytest.fixture(
    params=shopify_service.pipelines.values(),
    ids=shopify_service.pipelines.keys(),
)
def pipeline(request):
    return request.param


@pytest.fixture(
    params=shopify_service.shops.values(),
    ids=shopify_service.shops.keys(),
)
def shop(request):
    return request.param


class TestShopify:
    def test_service(self, pipeline, shop, timeframe):
        res = shopify_service.pipeline_service(
            pipeline,
            shop,
            timeframe[0],
            timeframe[1],
        )
        res


# def test_tasks(start, end):
#     res = run(
#         {
#             "tasks": "orders",
#             "start": start,
#             "end": end,
#         }
#     )
#     assert res["messages_sent"] > 0

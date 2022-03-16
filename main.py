from shopify.shopify_controller import shopify_controller
from tasks.tasks_service import tasks_service


def main(request):
    data = request.get_json()
    print(data)

    if "shop" in data:
        response = shopify_controller(data)
    else:
        response = tasks_service(data)

    print(response)
    return response

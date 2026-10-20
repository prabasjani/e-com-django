import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Product


@csrf_exempt
@require_http_methods(["POST"])
def create_product(request):
    data = json.loads(request.body)

    required_fields = ["product_name", "price", "description"]
    missing_fields = []

    for field in required_fields:
        if field not in data:
            missing_fields.append(field)

    if missing_fields:
        return JsonResponse({"error": "Some fields are missing..!"}, status=400)

    if data["price"] <= 0 or data["stock"] <= 0:
        return JsonResponse({"error": "Price and Stock can't be 0"}, status=400)

    if Product.objects.filter(product_name=data["product_name"]).exists():
        return JsonResponse({"message": "Product Already Exists!"})

    product = Product.objects.create(
        product_name=data["product_name"],
        price=data["price"],
        description=data["description"],
        stock=data["stock"],
    )

    new_product = {
        "id": product.id,
        "product name": product.product_name,
        "price": product.price,
        "description": product.description,
        "stock": product.stock,
        "created at": product.created_at,
    }

    return JsonResponse(
        {"message": "New Product Created", "product": new_product}, status=201
    )


@require_http_methods(["GET"])
def products_list(request):
    products = list(
        Product.objects.values(
            "id", "product_name", "price", "description", "stock", "created_at"
        )
    )

    if len(products) < 1:
        return JsonResponse({"error": "No Products Available"}, status=404)

    return JsonResponse(
        {
            "message": "Products Fetched Successfully",
            "products": products,
        },
        safe=False,
    )

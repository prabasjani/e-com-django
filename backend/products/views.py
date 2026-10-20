import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from django.core.exceptions import ValidationError

from .models import Product
from .helper import product_to_dict


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

    if data["price"] <= 0:
        return JsonResponse({"error": "Price can't be 0"}, status=400)

    if Product.objects.filter(product_name=data["product_name"]).exists():
        return JsonResponse({"message": "Product Already Exists!"})

    product = Product.objects.create(
        product_name=data["product_name"],
        price=data["price"],
        description=data["description"],
    )

    return JsonResponse(
        {"message": "New Product Created", "product": product_to_dict(product)},
        status=201,
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


@require_http_methods(["GET"])
def product_detail(request, product_id):

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product Not Found!"}, status=404)

    return JsonResponse(
        {
            "message": f"{product.product_name} details fetched",
            "product": product_to_dict(product),
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["PATCH"])
def update_product(request, product_id):
    product = Product.objects.filter(id=product_id).first()

    if product is None:
        return JsonResponse({"error": "Product Not Found!"}, status=404)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Something went wrong!"}, status=500)

    if "product_name" in data:
        product.product_name = data["product_name"].strip()

    if "price" in data:
        product.price = data["price"]

    if "description" in data:
        product.description = data["description"]

    if "stock" in data:
        product.stock = data["stock"]

    try:
        product.full_clean()
    except ValidationError as error:
        return JsonResponse({"errors": error.message_dict}, status=400)

    product.save()

    return JsonResponse(
        {
            "message": "Product updated successfully",
            "product": product_to_dict(product),
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_product(request, product_id):
    product = Product.objects.filter(id=product_id).first()

    if product is None:
        return JsonResponse({"error": "Product Not Found!"}, status=404)

    product.delete()
    return JsonResponse({"message": "Product Deleted!"}, status=200)

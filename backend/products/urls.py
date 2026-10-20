from django.urls import path

from .views import (
    create_product,
    products_list,
    product_detail,
    update_product,
    delete_product,
)

urlpatterns = [
    path("api/products/create", create_product, name="Create Product"),
    path("api/products", products_list, name="Products List"),
    path("api/products/<product_id>/", product_detail, name="Product Detail"),
    path("api/products/update/<product_id>/", update_product, name="Update Product"),
    path("api/products/delete/<product_id>/", delete_product, name="Delete Product"),
]

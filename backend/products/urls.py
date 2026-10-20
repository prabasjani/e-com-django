from django.urls import path

from .views import create_product, products_list

urlpatterns = [
    path("api/products/create", create_product, name="Create Product"),
    path("api/products", products_list, name="Products List"),
]

def product_to_dict(product):
    return {
        "id": product.id,
        "product_name": product.product_name,
        "price": product.price,
        "description": product.description,
        "stock": product.stock,
        "created_at": product.created_at.isoformat(),
    }

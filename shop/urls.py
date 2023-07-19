from django.urls import path
from .views import (
    products, product_detail, new_category, category_detail,
    categories, new_product, product_tags, review_product
)

app_name = 'shop'

urlpatterns = [
    path('review/<int:product_id>', review_product, name='review_product'),
    path('tagged/products/<tag>', product_tags, name='tagged_products'),
    path('new/product/<int:category_pk>', new_product, name='new_product'),
    path('categories', categories, name='categoriess'),
    path('category/<int:product_category_pk>', category_detail, name='category_detail'),
    path('new/category', new_category, name='new_category'),
    path('products', products, name='products'),
    path('product/<int:product_id>', product_detail, name='product_detail'),
]
from django.urls import path

from .views import cart_detail, cart_add, cart_remove, cart_clear, validate_cart, stock_short

app_name = 'cart'


urlpatterns = [
    path('stock/short/<int:product_pk>', stock_short, name='stock_short'),
    path('validate/cart', validate_cart, name='validate_cart'),
    path('cart/clear', cart_clear, name='cart_clear'),
    path('', cart_detail, name='cart_detail'),
    path('add/product/<int:product_id>', cart_add, name='cart_add'),
    path('remove/product/<int:product_id>', cart_remove, name='cart_remove'),

]

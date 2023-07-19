from django.urls import path
from shop.models import (
    Product,
)



from django.urls import path
from .views import (
    warning, order_create, created
)

app_name = 'orders'

urlpatterns = [
    path('order/created/<int:order_pk>', created, name='created'),
    path('order/create', order_create, name='order_create'),
    path('multiple/vendor/warning', warning, name='warning'),
]
from django.urls import path
from .views import (
    cash_payment, process_paystack, create_invoice
)

app_name = 'payments'


urlpatterns = [
    path('process/paystack/<int:order_id>', process_paystack, name='process_paystack'),
    path('cash/payment/<int:order_id>', cash_payment, name='cash_payment'),
    path('create/invoice/<int:order_id>', create_invoice, name='create_invoice'),
]
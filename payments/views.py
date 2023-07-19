from __future__ import unicode_literals, absolute_import
from django.shortcuts import render, redirect, get_object_or_404
import requests
from orders.models import Order
from weasyprint import HTML
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.db.models import (
    Count, Sum, Aggregate
)

def cash_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'payments/cash_invoice.html', {
        'order': order,
        'order_items': order.order_items
    })

def process_paystack(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    url = 'https://api.paystack.co/transaction/initialize'
    response = requests.post(url)
    return render(request, 'payments/start_pay.html', {
        'response': response,
        'order': order,
        'order_id': str(order.id)
    })

def create_invoice(request, order_id):
    totp = []
    order = get_object_or_404(Order, id=order_id)
    order_items = order.order_items
    total_products = sum(list(i.quantity for i in order.order_items.all()))
    response = HttpResponse(content_type='application/pdf')
    response['content-disposition'] = 'inline; filename=invoice.pdf'
    html = render_to_string('payments/invoice.html',{
        'order': order,
        'order_items': order_items,
        'total_products': total_products
    })
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)
    
    return response

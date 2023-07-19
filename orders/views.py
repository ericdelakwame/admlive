from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import OrderCreateForm
from .models import Order, OrderItem
from cart.cart import Cart
# from .tasks import (
    # notify_vendor, order_created,  create_cash_transaction, create_momo_transaction
# )

from collections import deque
import uuid

@login_required(login_url='accounts:login')
def order_create(request):
    tracking_no = uuid.uuid4()
    cart = Cart(request) 
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save()
            for item in cart:             
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price'],
                    
                )

        cart.clear()
        if order.payment_method == 'online':
                return redirect('payments:process_paystack', order.id)
        else:
            return redirect('payments:cash_payment',order.id)

    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html', {
        'cart': cart,
        'form': form,
       
        'form_header': 'Complete Your Order'
    })


def warning(request):
    return render(request, 'orders/warning.html', {

    })

def created(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    return render(request, 'orders/created.html', {
        'order': order,
        'order_items': order.order_items
    })

def stock_warning(request):
    return render(request, 'orders/stock_warning.html', {

    })
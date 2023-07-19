from django.shortcuts import (
    render, get_object_or_404, redirect
)

from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
# from djmoney.serializers import Serializer
import json
from django.http import HttpResponse

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        if product.stock < cd['quantity']:
            return redirect('cart:stock_short', product.pk)
        else:

            cart.add(
                product=product,
                quantity=cd['quantity'],
                update_quantity=cd['update'],

            )
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'update': True,

            }
        )

    return render(request, 'cart/detail.html', {
        'cart': cart,

    })


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'cart/detail.html', {

    })


def validate_cart(request):
    cart = Cart(request)
    return render(request, 'cart/validation.html', {
        'cart': cart
    })


def stock_short(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    return render(request, 'cart/stock_short.html', {
        'product': product,
    })
# from decimal import Decimal
from re import L
# import djmoney

from decimal import Decimal
# from djmoney.models.validators import Decimal
from django.conf import settings
# from djmoney.models.fields import MoneyField
from shop.models import Product
# from djmoney.money  import Money
# from djmoney.utils import get_amount
from django.db.models import Count, Sum
# from babel.numbers import format_currency, format_decimal, parse_number, get_global


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product
        for item in self.cart.values():
            price = item['price']
            prz = Decimal(price)
            item['total_price'] = prz * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
        # price= None
        # prz = None
        # import re
        # trim = re.compile(r'[^\d.,]+')
        # for i in self.cart.values():
        #     price = trim.sub('', i['price'])
         
            # price = p['price']
            # result = trim.sub('', price)
            # spr = result.strip("'")
            # ispr = int(spr)
        #     prz = Decimal(price)
        # return sum(prz* item['quantity'] for item in self.cart.values())
        
        

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

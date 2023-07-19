from django.db import models
from django.urls import reverse
from shop.models import Product
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.gis.db.models import PointField
from django.http import HttpResponse

User = get_user_model()


PAYMENT_CHOICES = (
    ('Online', 'Online'),
    ('Cash', 'Cash'),
)

class Order(models.Model):
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    email = models.EmailField()
    tel_no = PhoneNumberField()
    location = PointField()
    additional_instructions = models.CharField(max_length=100, default='')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    paid = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Order No {}: {} {}'.format(str(self.id), self.first_name, self.last_name)

    
    def get_absolute_url(self):
        return reverse('orders:order_detail', kwargs={'order_pk': self.pk})

    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.order_items.all())



class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return str(self.pk)

    def get_absolute_url(self):
        return reverse('orders:order_item_detail', kwargs={'order_item_pk': self.pk})

    def get_cost(self):
        print(self.product.name)
        return self.product.price*self.quantity

    # def save(self, *args, **kwargs):
    #     if self.product.total_stock > self.quantity:
    #         self.product.total_stock -= self.quantity
    #         self.product.save()
    #         super(OrderItem, self).save(*args, **kwargs)
    #     else:
    #         return HttpResponse('<div class="content"><h1 class="highlight">Not Enough Stock For Your Order</h1></div>')
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
User = get_user_model()


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category_detail', kwargs={'product_category_pk': self.pk})

class ProductImage(models.Model):
    image = models.ImageField(upload_to='product/images/%Y/%m/%d', null=True, blank=True)


class Product(models.Model):
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, related_name='products')
    product_image = models.ManyToManyField(ProductImage, related_name='product_images')
    name = models.CharField(max_length=100, unique=True)
    product_info = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='products/%Y/%m/%d', null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='products')
    created = models.DateTimeField(auto_now_add=True)
    stock = models.PositiveIntegerField(default=0)
    total_stock = models.PositiveIntegerField(default=0)
    tags = TaggableManager()
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'product_id': self.pk})

    def save(self, *args, **kwargs):
        if not self.pk:
            self.total_stock += stock
        super(Product, self).save(*args, **kwargs)


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='reviews')
    review = models.CharField(max_length=100)
    created  = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.review

from django import forms
from .models import (
    Product, ProductCategory, ProductImage, ProductReview
)


class ProductReviewForm(forms.ModelForm):


    class Meta:
        model = ProductReview
        fields = ['review'] 
        
           
class CategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name']


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['product_category', 'product_image', 'vendor', 'created']
from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    Product, ProductCategory, ProductImage, ProductReview
)
from .forms import (
    ProductForm, ProductImageForm, CategoryForm, ProductReviewForm
)
from cart.forms import CartAddProductForm
from taggit.models import Tag



def new_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect('shop:category_detail', category.pk)
    else:
        form = CategoryForm()
    return render(request, 'shop/forms/category_form.html', {
        'form': form,
        'form_header': 'Add A New Category'
    }) 


def categories(request):
    product_categories = ProductCategory.objects.order_by('-name')
    return render(request, 'shop/categories.html', {
        'product_categories': product_categories
    })

def category_detail(request, product_category_pk):
    category = get_object_or_404(ProductCategory, pk=product_category_pk)
    return render(request, 'shop/category_detail.html', {
        'product_category': category
    })



def new_product(request, category_pk):
    category = get_object_or_404(ProductCategory, pk=category_pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.product_category = category
            product.vendor = request.user
            product.save()
            form.save_m2m()
            return redirect('shop:product_detail', product.pk)
    else:
        form = ProductForm()
    return render(request, 'shop/forms/product_form.html', {
        'form': form,
        'form_header': 'Add A New Product To {}'.format(category)
    }) 


def products(request):
    product_categories = ProductCategory.objects.order_by('-name')
    products = Product.objects.prefetch_related('product_category').order_by('-name')
    return render(request, 'shop/products.html', {
        'products': products,
        'product_categories': product_categories
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    other_products = Product.objects.exclude(id=product.id)
    cart_product_form = CartAddProductForm()
    review_form = ProductReviewForm()
    return render(request, 'shop/product_detail.html', {
            'product': product,
            'cart_product_form': cart_product_form,
            'other_products': other_products,
            'product_id': str(product.id),
            'review_form': review_form,
    }
    )
def product_tags(request, tag):
    products = Product.objects.filter(tags__name__icontains=tag)
    return render(request, 'shop/tagged_products.html', {
        'products': products,
        'tag': tag
    })

def review_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.order_by('-created')
    if request.method == 'POST':
        form = ProductReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.product = product
            review.save()
            return redirect('shop:product_detail', product.id)
    else:
        form = ProductReviewForm()
    return render(request, 'shop/product_detail.html', {
        'review_form': form,
        'product': product,
        'reviews': reviews
    })
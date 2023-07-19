from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from blog.models import (
    Post, Comment, PostImage, PostReply
)
from studio.models import (Category, Project, ProjectImage)
from student.models import StudentProject
from shop.models import Product, ProductCategory
from orders.models import Order, OrderItem
from accounts.forms import ModeratorRequestForm
from django.db.models import Max, Count, Avg, Sum
from django.conf import settings


User = get_user_model()


slack_client_id = settings.SLACK_CLIENT_ID


def moderator_pass(user):
    if user.is_moderator:
        return True
    else:
        return False

@login_required
@user_passes_test(moderator_pass)
def index(request):
    add_to_slack = "https://slack.com/oauth/authorize?scope=bot&client_id={}".format(
        slack_client_id)
    sold_list = []
    sold_data = {}
    products_sold = OrderItem.objects.values(
        'product__name').annotate(Max('quantity'))
    for i in products_sold:
        sold_data['product'] = i['product__name']
        sold_data['quantity'] = i['quantity__max']
        sold_list.append(sold_data)
    orders = Order.objects.order_by('-created')
    projects = Project.objects.all()
    student_projects = StudentProject.objects.all()
    posts = Post.objects.order_by('-created')
    blog_comments = Comment.objects.select_related(
        'post').order_by('-created')[0:9]
    products = Product.objects.all()
    product_categories = ProductCategory.objects.all()
    users = User.objects.all()
    pending_activations = User.objects.filter(activated=False).order_by('-date_joined')
    return render(request, 'moderator/dashboard.html', {
        'users': users,
        'blog_posts': posts,
        'projects': projects,
        'student_projects': student_projects,
        'latest_projects': Project.objects.order_by('-created')[0:5],
        'my_projects': Project.objects.filter(owner=request.user),
        'pending_activations': pending_activations,
        'orders': orders,
        'order_items': OrderItem.objects.order_by('-created'),
        'products': products,
        'product_categories': product_categories,
        'sold_list': sold_list[0:2],
        'slack_btn': add_to_slack

    })


@user_passes_test(moderator_pass)
def users(request):
    users = User.objects.order_by('-last_name')
    return render(request, 'moderator/users.html', {
        'users': users
    })


@user_passes_test(moderator_pass)
def user_detail(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    return render(request, 'moderator/user_detail.html', {
        'user': user
    })

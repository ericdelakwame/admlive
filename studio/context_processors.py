from django.contrib.auth import get_user_model
from .models import Project, Category, MainCategory

User = get_user_model()

def site_users(request):
    site_users = User.objects.order_by('first_name')
    return {'site_users': site_users}

def top_categories(request):
    top_categories = MainCategory.objects.order_by('name')
    return {'top_categories': top_categories}


def categories(request):
    categories = Category.objects.order_by('name')
    return {'categories': categories}

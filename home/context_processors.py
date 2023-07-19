from .models import Post


def site_posts(request):
    return {
        'site_posts': Post.objects.order_by('-created')
    }

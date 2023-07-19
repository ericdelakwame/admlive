from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serilaizers import PostSerializer
from blog.models import Post, Comment


class PostViewset(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    queryset = Post.objects.order_by('-created')
    serializer_class = PostSerializer
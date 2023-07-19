from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .accounts.views import (
    UserViewset
)
from .studio.views import (
    ProjectViewset
)
from .blog.views import PostViewset

router = DefaultRouter()

router.register('posts', PostViewset, basename='posts')
router.register('projects', ProjectViewset, basename='projects')
router.register('users', UserViewset, basename='users' )

urlpatterns = [
    path('blog/', include(router.urls)),
    path('accounts/', include(router.urls)),
    path('studio/', include(router.urls)),
]

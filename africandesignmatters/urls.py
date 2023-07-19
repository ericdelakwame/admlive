from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from blog.models import Post


info_dict= {
    "queryset": Post.objects.all(),
}



router = DefaultRouter()
router.register('devices', FCMDeviceAuthorizedViewSet)





urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('', include('pwa.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': {'blog': GenericSitemap(info_dict, priority=0.6)}},
         name='django.contrib.sitemaps.views.sitemap'),
    path('adm_slack/', include('adm_slack.urls')),
    path('moderator/', include('moderator.urls')),
    path('api/', include(router.urls)),
    # path("firebase-messaging-sw.js",
    #     TemplateView.as_view(
    #         template_name="firebase-messaging-sw.js",
    #         content_type="application/javascript",
    #     ),
    #     name="firebase-messaging-sw.js"
    # ),
    path('student/', include('student.urls')),
    path('orders/', include('orders.urls')),
    path('cart/', include('cart.urls')),
    path('shop/', include('shop.urls')),
    path('api/', include('api.urls')),
    path('studio/', include('studio.urls')),
    path('blog/', include('blog.urls')),
    path('payments/', include('payments.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('dashboard/', include('dashboard.urls')),
    # path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/javascript'), name='sw.js'),
    path('', include('home.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)


handler404 = 'home.views.error_404'

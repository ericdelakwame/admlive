from django.urls import path
from .views import (
    posts, post_detail, new_post, post_reply
)
app_name = 'blog'



urlpatterns = [
    path('reply/<int:comment_pk>', post_reply, name='reply'),
    path('new/post', new_post, name='new_post'),
    path('posts', posts, name='posts'),
    path('post/<int:post_pk>', post_detail, name='post_detail'),
]
from django.urls import path
from .views import (
    index, users, user_detail
)
app_name= 'moderator'

urlpatterns = [
    path('users', users, name='users'),
    path('user/<int:user_pk>', user_detail, name='user_detail'),
    path('', index, name='index'),
]
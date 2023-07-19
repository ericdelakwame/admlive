from django.urls import path
from .views import (
     index, channel_members, slack_user_detail, create_channel, list_channels, channel_detail, invite_channel_users, 
)
app_name = 'adm_slack'


urlpatterns = [
    path('invite/users/<int:invitation_id>', invite_channel_users, name='invite_channel_users'),
    path('channel/<channel_id>', channel_detail, name='channel_detail'),
    path('list/channels', list_channels, name='list_channels'),
    path('create/channel', create_channel, name='create_channel'),
    path('slack/user/detail/<user_id>', slack_user_detail, name='slack_user_detail'),
    path('', index, name='index'),
    path('members/channel/<channel>', channel_members, name='channel_members'),
]
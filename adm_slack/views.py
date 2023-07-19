from django.shortcuts import render, redirect, get_object_or_404
from .models import SlackChannel, SlackUser, SlackInvitation
from slack_sdk import WebClient
from django.conf import settings
from adm_slack.forms import SlackChannelForm, SlackInvitationForm, InvitationListForm
from django.contrib.auth.decorators import (
    login_required, user_passes_test
)

slack_app_token = settings.SLACK_APP_TOKEN
slack_token = settings.SLACK_AUTH_TOKEN


@login_required(login_url='accounts:login')
def index(request):
    slack_channels = SlackChannel.objects.order_by('-name')
    return render(request, 'adm_slack/index.html', {
        'slack_channels': slack_channels
    })


def create_channel(request):
    client = WebClient(token=slack_token)
    if request.method == 'POST':
        form = SlackChannelForm(request.POST)
        if  form.is_valid():
            channel = form.save()
            response = client.conversations_create(name=channel.name)
            return redirect('adm_slack:list_channels')
    else:
        form = SlackChannelForm()
    return render(request, 'adm_slack/forms/slack_channel_form.html', {
        'form': form
    })


def list_channels(request):
    client = WebClient(token=slack_token)
    response = client.conversations_list()
    channels = response['channels']
    return render(request, 'adm_slack/list_channels.html', {
        'channels': channels
    })

def channel_detail(request, channel_id):
    invitees = None
    slack_users = None
    client = WebClient(token=slack_token)
    response = client.users_list()
    users = response['members']
    for user in users:
        user_profile = user['profile']
        user_id = user['id']
        real_name = user_profile['real_name']
        slack_users, created = SlackUser.objects.get_or_create(user_id=user_id, name=real_name)
    slack_users = SlackUser.objects.all()
    response = client.conversations_info(channel=channel_id)
    channel = response['channel']
    channel_name = channel["id"]

    if request.method == 'POST':
        form = SlackInvitationForm(request.POST, request.FILES)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.channel=channel_name
            invitation.save()
            for slack_user in slack_users:
                invitation.invited_users.add(slack_user)
            form.save_m2m()
            
    else:
        form = SlackInvitationForm()            
    return render(request, 'adm_slack/channel_detail.html', {
        'channel': channel,
        'form': form,
        'slack_users': slack_users
    })

def invite_channel_users(request, invitation_id):
    invitees = []
    invitation = get_object_or_404(SlackInvitation, id=invitation_id)
    invitation_channel = invitation.channel
    client = WebClient(token=slack_token)
    response = client.conversations_info(channel=invitation.channel)
    channel = response['channel']
    channel_id = channel['id']
    for user in invitation.invited_users.all():
        user_id = user.user_id
        invitees.append(user_id)
    print(invitees)
    slack_invitation = client.conversations_invite(channel=channel_id, users=invitees)
    return redirect('adm_slack:channel_members', channel)
    
def channel_members(request, channel):
    client = WebClient(token=slack_token)
    response = client.conversations_members(channel=channel)
    members = response['members']
    return render(request, 'adm_slack/members.html', {
        'members': members,
        'channel': channel
    })

def slack_user_detail(request, user_id):
    client = WebClient(token=slack_token)
    user = client.users_profile_get(user=user_id)
    return render(request, 'adm_slack/user_detail.html', {
        'user': user
    })

def join_conversation(request, channel):
    channel = get_object_or_404(SlackChannel, name=channel)
    client = WebClient(token=slack_token)
    client.conversations_join(channel=channel)

    
# Events

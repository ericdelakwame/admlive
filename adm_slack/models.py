from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Moderator, Student, Designer


User = get_user_model()

class SlackChannel(models.Model):
    name = models.CharField(max_length=50, default='', unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('adm_slack:channel_detail', kwargs={'channel_pk': self.pk})

    def __str__(self):
        return self.name

class SlackUser(models.Model):
    user_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    def __str__(self):
        return '{} , Id: {}'.format(self.name, self.user_id)

    def get_absolute_url(self):
        return reverse('adm_slack:slack_user_detail', kwargs={'slack_user_pk': self.pk})

class SlackInvitation(models.Model):
    channel = models.CharField(max_length=50)
    invitation_date = models.DateTimeField(auto_now_add=True)
    invited_users = models.ManyToManyField(SlackUser, related_name='invitees')
    

    def __str__(self):
        return self.channel


class InvitationList(models.Model):
    slack_user = models.CharField(max_length=50)
    channel = models.CharField(max_length=50)

    def __str__(self):
        return self.slack_user
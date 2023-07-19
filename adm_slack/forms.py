from django import forms
from .models import SlackChannel, SlackInvitation, InvitationList, SlackUser
from django.contrib.auth import get_user_model


User = get_user_model()

class SlackChannelForm(forms.ModelForm):

    class Meta:
        model = SlackChannel
        fields = ['name']


class SlackInvitationForm(forms.ModelForm):
    invited_users = forms.ModelMultipleChoiceField(label='Users To Invitee', widget=forms.CheckboxSelectMultiple() ,queryset=SlackUser.objects.all())
    class Meta:
        model = SlackInvitation
        fields = ['invited_users']

class InvitationListForm(forms.ModelForm):

    class Meta:
        model = InvitationList
        fields = ['slack_user']
from django import forms
from django.conf import settings
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm
)
from mapwidgets.widgets import GooglePointFieldWidget
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.gis.forms import PointField
from .models import (
    Profile, Moderator, Admin, Designer, Community, ModeratorRequest, Task, Student, User
)
from studio.models import Category
from .choices import CONTINENT_CHOICES, GENDER_CHOICES, ETHNICITY_CHOICES
from django.contrib.auth import get_user_model

User = get_user_model()

class NewUserForm(UserCreationForm):
    tel_no = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'placeholder': 'Tel No: Eg: 2411111'}), label='Country Code', initial='+233')
    location = PointField(widget=GooglePointFieldWidget())
    gender = forms.ChoiceField(label='Choose Gender', choices=GENDER_CHOICES, widget=forms.RadioSelect(attrs={'class': 'radio'}))
    ethnicity = forms.ChoiceField(label='Which of these best describes your ethnicity?', choices=ETHNICITY_CHOICES, widget=forms.RadioSelect(attrs={'class': 'radio'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'instagram_handle', 'tel_no', 'gender', 'ethnicity', 'country', 'photo',  'location' ,'password1']

class StudentForm(UserCreationForm):
    tel_no = PhoneNumberField(widget=PhoneNumberPrefixWidget(
        attrs={'placeholder': 'Tel No: Eg: 2411111'}), label='Country Code', initial='+233')
    location = PointField(widget=GooglePointFieldWidget())
    gender = forms.ChoiceField(
        label='Choose Gender', choices=GENDER_CHOICES, widget=forms.RadioSelect())
    ethnicity = forms.ChoiceField(label='Which of these best describes your ethnicity?',
                                  choices=ETHNICITY_CHOICES, widget=forms.RadioSelect())
    institution = forms.CharField(label='Name Of Institution')

    class Meta:
        model = Student
        fields = ['username', 'first_name', 'last_name', 'email', 'tel_no', 'instagram_handle', 'institution',
                   'gender', 'ethnicity', 'country', 'photo',  'location', 'password1']
 
class ProfileForm(forms.ModelForm):
    specialty = forms.ModelMultipleChoiceField(queryset=Category.objects.order_by('-name'), widget=forms.CheckboxSelectMultiple(attrs={'class': 'check'}))
    
    class Meta:
        model = Profile
        exclude = ['user']

class CommunityForm(forms.ModelForm):
    area = forms.ChoiceField(widget=forms.RadioSelect(), choices=CONTINENT_CHOICES)

    class Meta:
        model = Community
        fields = ['name', 'area', 'rules', 'banner']

class ModeratorRequestForm(forms.ModelForm):

    class Meta:
        model = ModeratorRequest
        fields = ['message']


class TaskForm(forms.ModelForm):
    due_date = forms.DateField(widget=forms.DateInput(attrs={'id': 'date', 'placeholder':'M/D/Year'}))

    class Meta:
        model = Task
        fields = ['new_task', 'due_date']

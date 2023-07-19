from django import forms
from .models import PostImage, PressNote
from home.models import AboutImage, AboutNote, Resource



class PressNoteForm(forms.ModelForm):
    
    class Meta:
        model = PressNote
        fields = '__all__'

class AboutNoteForm(forms.ModelForm):
    # images = forms.ImageField(required=False)
    
    class Meta:
        model = AboutNote
        exclude = ['created', 'images']


class AboutImageForm(forms.ModelForm):

    class Meta:
        model = AboutImage
        fields = ['image']


class ResourceForm(forms.ModelForm):

    class Meta:
        model = Resource
        fields = ['content']

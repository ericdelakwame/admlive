from django import forms
from .models import (
     Category, ProjectImage, Project, Review, MainCategory
)

from embed_video.fields import EmbedVideoFormField

class MainCategoryForm(forms.ModelForm):

    class Meta:
        model = MainCategory
        fields = ['name']

        
class ProjectImageForm(forms.ModelForm):

    class Meta:
        model = ProjectImage
        fields = ['image']


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'category_info', 'image']

class ProjectForm(forms.ModelForm):
    name = forms.CharField(label='Name Your Project')
    intro = forms.TextInput(attrs={
        'placeholder': 'Brief Intro To Your Project', 'rows': 10, 'cols': 15})
    video = EmbedVideoFormField(widget=forms.TextInput(attrs={'placeholder':'Enter Video URL'}), label='Embed Video')
    description = forms.TextInput(attrs={'placeholder': 'Describe Your project'})
    

    class Meta:
        model = Project
        exclude = ['owner', 'created', 'images', 'category']


class ReviewForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Review this project'}), label='Add a review')
    class Meta:
        model = Review
        fields = ['content']
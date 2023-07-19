from django import forms
from .models import (
    Post, Comment, PostImage, PostReply
) 

from embed_video.fields import EmbedVideoFormField

class PostImageForm(forms.ModelForm):    

    class Meta:
        model = PostImage
        fields = ['image']
        

class PostForm(forms.ModelForm):
    video = EmbedVideoFormField(widget=forms.TextInput(attrs={'placeholder': 'Place video link here '}), label='Embed Video')
    
    class Meta:
        model = Post
        exclude = ['author', 'images', 'created', 'publish']


class CommentForm(forms.ModelForm):
    content = forms.CharField(label='Message', widget=forms.Textarea())
    class Meta:
        model = Comment
        exclude = ['author', 'created', 'post', 'publish']


class PostReplyForm(forms.ModelForm):

    class Meta:
        model = PostReply
        exclude = ['author', 'comment', 'created', ]

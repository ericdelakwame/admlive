from rest_framework.serializers import ModelSerializer
from blog.models import Post, Comment
from django.contrib.auth import get_user_model
from taggit_serializer.serializers import (TaggitSerializer, TagListSerializerField)
User = get_user_model()



class AuthorSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(TaggitSerializer, ModelSerializer):
    author = AuthorSerializer()
    comments = CommentSerializer(many=True)
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = '__all__'



from django.db import models
from django.urls import reverse
from django.conf import settings
from taggit.managers import TaggableManager
from embed_video.fields import EmbedVideoField
from tinymce.models import HTMLField

User = settings.AUTH_USER_MODEL


class PostImage(models.Model):
    image = models.ImageField(upload_to='post_images/%Y/%m/%d', null=True)

class PostParagraph(models.Model):
    image = models.ImageField(upload_to='%Y/%m/%d', null=True, blank=True)
    paragraph = models.TextField(default='')


class Post(models.Model):
    heading = models.CharField(max_length=100)
    subheading = models.TextField(default='', blank=True)
    content = HTMLField(blank=True, default='')
    image = models.ImageField(upload_to='blog/posts/%Y/%m/%d',null=True, blank=True )
    video = EmbedVideoField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='posts')
    images = models.ManyToManyField(PostImage, related_name='post_images')
    publish = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return '{} {}'.format(self.heading, self.author.get_full_name)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'post_pk': self.pk})

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name='comments')
    content = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    publish = models.BooleanField(default=False)

class PostReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, related_name='replies')
    reply = models.CharField(max_length=100, default='')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='replies')
    created = models.DateTimeField(auto_now_add=True)

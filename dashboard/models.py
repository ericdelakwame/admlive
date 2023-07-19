from django.db import models
from django.urls import reverse
from accounts.models import User
from tinymce.models import HTMLField

class PostImage(models.Model):
    image = models.ImageField(upload_to='admin/post/images/%Y/%m/%d', null=True, blank=True)


class PressNote(models.Model):
    date = models.CharField(max_length=50)
    content = HTMLField(blank=True)
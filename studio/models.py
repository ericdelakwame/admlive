from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager
from hitcount.models import HitCountMixin
from hitcount.settings import MODEL_HITCOUNT
from embed_video.fields import EmbedVideoField
User = settings.AUTH_USER_MODEL

CATEGORY_CHOICES = (
    ('Design', 'Design'),
    ('Seventh Art', 'Seventh Art'),
)

class MainCategory(models.Model):
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='', unique=True)
    image = models.ImageField(upload_to='main/categories/%Y/%m/%d', null=True, blank=True)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('studio:main_category_detail', kwargs={'main_category_pk': self.pk})


class Category(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, null=True, related_name='categories')
    name = models.CharField(max_length=100, unique=True)
    category_info = models.TextField(default='')
    image = models.ImageField(upload_to='categories/%Y/%m/%d', null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('studio:category_detail', kwargs={'category_pk': self.pk})


class ProjectImage(models.Model):
    image = models.ImageField(
        upload_to='project/images/%Y/%m/%d', null=True, blank=True)



class Project(models.Model, HitCountMixin):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, related_name='projects')
    name = models.CharField(max_length=100, default='', unique=True)
    location = models.CharField(max_length=100, default='')
    description = models.TextField()
    image = models.ImageField(
        upload_to='project/images/%Y/%m/%d', null=True, blank=True)
    video = EmbedVideoField(blank=True, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='projects')
    images = models.ManyToManyField(
        ProjectImage, related_name='project_images')
    created = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    hit_count_generic = GenericRelation(MODEL_HITCOUNT, object_id_field='object_pk', related_query_name='hit_count_relation')    

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return '{}: {}'.format(self.name, self.owner.get_full_name())

    def get_absolute_url(self):
        return reverse('studio:project_detail', kwargs={'pk': self.pk})


class Review(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='reviews')
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, related_name='reviews')
    created = models.DateTimeField(auto_now_add=True)

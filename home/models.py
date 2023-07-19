from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField


class AboutImage(models.Model):
    image = models.ImageField(
        upload_to='about_images/%Y/%m/%d', null=True, blank=True)

class AboutNote(models.Model):
    image = models.ImageField(
        upload_to='about/%Y/%m/%d', null=True, blank=True)
    image_caption = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=100, default='', blank=True)
    subtitle = models.CharField(max_length=100, default='', blank=True)
    body = HTMLField(default='', blank=True)
    paragraph_caption = models.CharField(max_length=100, default='')
    paragraph_text = HTMLField(blank=True, null=True)
    paragraph_image = models.ImageField(upload_to='manifesto/%Y/%m/%d', null=True, blank=True)
   
    created = models.DateTimeField(auto_now_add=True)
    images = models.ManyToManyField(AboutImage, related_name='about_images', blank=True)
    
    class Meta:
        verbose_name = 'Manifesto Note'
        verbose_name_plural = 'Manifesto Notes'

    def __str__(self):
        return '{} created on {}'.format(self.title, str(self.created))

    def get_absolute_url(self):
        return reverse('home:about_detail', kwargs={'about_pk': self.pk})

class Resource(models.Model):
    content = HTMLField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Resource'
        verbose_name_plural = 'Resources'
    
    def __str__(self):
        return self.created

    def get_absolute_url(self):
        return reverse('home:resource_pk', kwargs={'resource_pk': self.pk})

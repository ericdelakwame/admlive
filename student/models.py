from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Student
from taggit.managers import TaggableManager
from hitcount.models import HitCountMixin
from hitcount.settings import MODEL_HITCOUNT
from django.contrib.contenttypes.fields import GenericRelation
User = get_user_model()

class ProjectImage(models.Model):
    image = models.ImageField(upload_to='student/%Y/%m/%d', null=True, blank=True)

class StudentProject(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='student/%Y/%m/%d', null=True, blank=True)
    images = models.ManyToManyField(ProjectImage, related_name='project_images')
    intro = models.CharField(max_length=100, default='')
    description = models.TextField()
    owner = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name='student_projects')
    tags = TaggableManager()
    hit_count_generic = GenericRelation(
        MODEL_HITCOUNT, object_id_field='object_pk', related_query_name='hit_count_relation')
    created = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return 'Student Project By {}'.format(self.name)

    def get_absolute_url(self):
        return reverse('student:project_detail', kwargs={'project_pk': self.pk})

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.gis.db.models import PointField
from studio.models import Category
from .choices import CONTINENT_CHOICES, GENDER_CHOICES, ETHNICITY_CHOICES
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_paragon = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    is_designer = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    activated = models.BooleanField(default=False)
    tel_no = PhoneNumberField(blank=True, null=True)
    location = PointField(null=True)
    photo = models.ImageField(
        upload_to='users/%Y/%m/%d', null=True, blank=True)
    connected_users = models.ManyToManyField('self', related_name='network')
    gender = models.CharField(
        max_length=20, default='', choices=GENDER_CHOICES)
    ethnicity = models.CharField(
        max_length=50, default='', choices=ETHNICITY_CHOICES)
    country = models.CharField(max_length=100, default='')
    instagram_handle = models.CharField(max_length=100,default='')

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('accounts:user_detail', kwargs={'user_pk': self.pk})

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Admin(User):
    pass

    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admin'

    def __str__(self):
        return '{}: Admin'.format(self.get_full_name())


class Designer(User):
    pass

    class Meta:
        verbose_name = 'Designer'
        verbose_name_plural = 'Designers'

    def __str__(self):
        return '{}: Designer'.format(self.get_full_name())


class Moderator(User):
    pass

    class Meta:
        verbose_name = 'Moderator'
        verbose_name_plural = 'Moderators'

    def __str__(self):
        return '{}: Moderator'.format(self.get_full_name())


class Student(User):
    institution = models.CharField(max_length=100)
    network = models.ManyToManyField(User, related_name='student_network')

    class Meta:
        permissions = (
            ('can_add_studentproject', 'Can Add Student Project'),
           )
            
        

    def __str__(self):
        return '{}: Student, {}'.format(self.get_full_name(), self.institution)

    def get_absolute_url(self):
        return reverse('home:student_detail', kwargs={'student_pk': self.pk})


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, related_name='profile')
    company_name = models.CharField(max_length=100, default='')
    logo = models.ImageField(
        upload_to='profile/logos/%Y/%m/%d', null=True, blank=True)
    specialty = models.ManyToManyField(Category)
    bio = models.TextField(blank=True)
    about = models.TextField(blank=True)
    banner = models.ImageField(
        upload_to='profile/banners/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.user.first_name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('accounts:user_profile', kwargs={'user_pk': self.pk})


class Community(models.Model):
    area = models.CharField(choices=CONTINENT_CHOICES,
                            max_length=100, default='')
    name = models.CharField(max_length=100)
    rules = models.TextField(blank=True)
    banner = models.ImageField(
        upload_to='communities/%Y/%m/%d', null=True, blank=True)
    moderator = models.ForeignKey(
        Moderator, on_delete=models.CASCADE, null=True)
    members = models.ManyToManyField(User, related_name='community_members')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('studio:community_detail', kwargs={'community_pk': self.pk})


class ModeratorRequest(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='user_requests')
    created = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return '{} requested to be a moderator'.format(user.get_full_name())

    def get_absolute_url(self):
        return reverse('accounts:moderator_request_detail', kwargs={'moderator_request_pk': self.pk})


class Task(models.Model):
    user = models.ForeignKey(User, related_name='tasks',
                             on_delete=models.CASCADE, null=True)
    new_task = models.CharField(max_length=100, default='')
    due_date = models.DateField(null=True)
    completed = models.BooleanField(default=False)


class Network(models.Model):
    users = models.ManyToManyField(User, related_name='friends')

    def __str__(self):
        return '{} in network'.format(str(len(users)))


def create_profile(sender, instance, **kwargs):
    profile, created = Profile.objects.get_or_create(user=instance)


post_save.connect(create_profile, sender=User)

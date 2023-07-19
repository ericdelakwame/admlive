from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Moderator, Student, Designer


admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(Moderator)
admin.site.register(Designer)

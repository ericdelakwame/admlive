from django.contrib import admin
from studio.models import (
    MainCategory, Category, Project
)


admin.site.register(Project)
admin.site.register(MainCategory)
admin.site.register(Category)

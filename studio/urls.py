from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    index, new_project, project_categories,
    category_detail, project_tags, designer, moderator, projects, new_category, users, user_detail, new_main_category, main_categories, main_category_detail,
    ProjectDetailView, my_projects, project_categories, my_projects, ProjectUpdateView, ProjectDelete, review_project, new_project_image, search_projects,
)

app_name = 'studio'


urlpatterns = [
    
    path('search/projects', search_projects, name='search_projects'),
    path('new/project/image/<int:project_pk>', new_project_image, name='new_project_image'),
    path('review/project/<int:project_pk>', review_project, name='review_project'),
    path('delete/project/<pk>', ProjectDelete.as_view(), name='delete_project'),
    path('update/project/<pk>', ProjectUpdateView.as_view(), name='update_project'),
    path('my/projects/<int:user_pk>', my_projects, name='my_projects'),
    path('project/categories', project_categories,name='project_categories'),
    path('my/projects/<int:user_pk>', my_projects, name='my_projects'),
    path('project/<int:pk>', ProjectDetailView.as_view(template_name='studio/project_detail.html'), name='project_detail'),
    path('main/category/<int:main_category_pk>', main_category_detail, name='main_category_detail'),
    path('main/categories', main_categories, name='main_categories'),
    path('new/main/category', new_main_category, name='new_main_category'),
    path('user/<int:user_pk>', user_detail, name='user_detail'),
    path('users', users, name='users'),
    path('new/category/<int:main_category_pk>', new_category, name='new_category'),
    path('projects', projects, name='projects'),
    path('moderator', moderator, name='moderator'),
    path('designer', designer, name='designer'),
    path('project/tags/<tag>', project_tags, name='project_tags'),
    path('category/<int:category_pk>', category_detail,name='category_detail'),
    path('categories', project_categories, name='categories'),
    # path('project/<int:project_pk>', project_detail, name='project_detail'),
    path('', index, name='index'),
    path('new/project/<int:category_pk>', new_project, name='new_project'),

    
]
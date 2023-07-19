from django.urls import path
from .views import (
    index,  about, user_profile, article_detail, search,
    nearby_view, send_message, ethnicity_filter, gender_filter, other_filter, filter_paragon, student_project_detail, contact, directory, admcopyright, directory_category, dir_filter, press, resources

    )

app_name = 'home'




urlpatterns = [
    path('resources', resources, name='resources'),
    path('press', press, name='press'),
    path('directory/filter', dir_filter, name='dir_filter'),
    path('directory/category/<int:category_pk>', directory_category, name='directory_category'),
    path('copyright', admcopyright, name='copyright'),
    path('directory', directory, name='directory'),
    path('contact', contact, name='contact'),
    path('student/project/<int:project_pk>', student_project_detail, name='student_project_detail'),
    path('filter/paragon/<verb>', filter_paragon, name='filter_paragon'),
    path('other/filter/<verb>', other_filter, name='other_filter'),
    path('filter/by/gender/<verb>', gender_filter, name='gender_filter'),
    path('filter/by/ethnicity/<verb>', ethnicity_filter, name='ethnicity_filter'),
    # path('send/message', send_message, name='send_message'),
    path('nearby/view', nearby_view, name='nearby_view'),
    path('search', search, name='search'),
    path('article/<int:article_pk>', article_detail, name='article_detail'),
    path('user/profile/<int:user_pk>', user_profile, name='user_profile'),
    path('', index, name='index'),
    path('about', about, name='about'),
]

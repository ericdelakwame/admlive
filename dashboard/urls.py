from django.urls import path
from .views import (
    index, users, user_detail, new_project_category, category_detail, review_mod_request, accept_mod_request,
    reject_mod_request, activate_user, deactivate_user,
    projects, new_main_category, main_categories, main_category_detail, publish_comment, remove_comment,
    new_post, post_detail, UpdatePostView, DeletePostView,
    remove_task, posts, post_images, publish_all_comments, ethnicity_view, gender_view, enable_paragon, slack, list_slack_channels, create_channel, enable_moderator, disable_moderator, UpdateCategoryView, categories, add_about_note, about_note_detail, new_press, press_detail, new_resource, resource_detail, UpdateResourceView, DeleteResourceView, UpdatePressView, DeletePressView, press_notes, resources

)

app_name = 'dashboard'


urlpatterns = [
    path('press/notes', press_notes, name='press_notes'),
    path('resources', resources, name='resources'),
    path('delete/press/<int:pk>', DeletePressView.as_view(), name='delete_press'),
    path('update/press/<int:pk>',
         UpdatePressView.as_view(), name='update_press'),
    path('delete/resource/<int:pk>', DeleteResourceView.as_view(), name='delete_resource'),
    path('update/resource/<int:pk>',
         UpdateResourceView.as_view(), name='update_resource'),
    path('resource/<int:resource_pk>', resource_detail, name='resource_detail'),
    path('new/resource', new_resource, name='new_resource'),
    path('press/<int:press_pk>', press_detail, name='press_detail'),
    path('new/press', new_press, name='new_press'),
    path('add/about/note', add_about_note, name='add_about_note'),
    path('about/note/<int:about_pk>', about_note_detail, name='about_note_detail'),
    path('categories', categories, name='categories'),
    path('update/category/<int:pk>',
         UpdateCategoryView.as_view(), name='update_category'),
    path('enable/moderator/<int:user_pk>',
         enable_moderator, name='enable_moderator'),
    path('disable/moderator/<int:user_pk>',
         disable_moderator, name='disable_moderator'),
    path('create/channel', create_channel, name='create_channel'),
    path('list/slack/channels', list_slack_channels, name='list_slack_channels'),
    path('slack', slack, name='slack'),
    path('enable/paragon/<int:user_pk>', enable_paragon, name='enable_paragon'),
    path('gender/view', gender_view, name='gender_view'),
    path('ethnicity/view', ethnicity_view, name='ethnicity_view'),
    path('publish/all/comments', publish_all_comments, name='publish_comments'),
    path('post/images/<int:post_pk>', post_images, name='post_images'),
    path('posts', posts, name='posts'),
    path('remove/task/<int:task_pk>', remove_task, name='remove_task'),
    path('update/<int:pk>', UpdatePostView.as_view(), name='update_post'),
    path('delete/<int:pk>', DeletePostView.as_view(), name='delete_post'),
    path('new/post', new_post, name='new_post'),
    path('post/<int:post_pk>', post_detail, name='post_detail'),
    path('publish/comment/<int:comment_pk>',
         publish_comment, name='publish_comment'),
    path('remove/comment/<int:comment_pk>',
         remove_comment, name='remove_comment'),
    path('main/categories', main_categories, name='main_categories'),
    path('new/top/category', new_main_category, name='new_main_category'),
    path('main/category/<int:topcat_pk>',
         main_category_detail, name='main_category_detail'),
    path('projects', projects, name='projects'),
    path('activate/<int:user_pk>', activate_user, name='activate_user'),
    path('deactivate/<int:user_pk>', deactivate_user, name='deactivate_user'),
    path('reject/mod/request/<int:mod_request_pk>',
         reject_mod_request, name='reject_mod_request'),
    path('accept/mod/request/<int:mod_request_pk>',
         accept_mod_request, name='accept_mod_request'),
    path('review/mod/request/<int:mod_request_pk>',
         review_mod_request, name='review_mod_request'),
    path('project/category/<int:category_pk>',
         category_detail, name='category_detail'),
    path('new/project/category/<int:topcat_pk>',
         new_project_category, name='new_project_category'),

    path('', index, name='index'),
    path('users', users, name='users'),
    path('user/<int:user_pk>', user_detail, name='user_detail'),

]
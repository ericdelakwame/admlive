from django.urls import path
from .views import (
    index, project_detail, new_student_project, add_project_image, UpdateProjectView, DeleteProjectView, add_project_image, my_projects, connect_with_user
)


app_name = 'student'


urlpatterns = [
    path('connect/<int:user_pk>', connect_with_user, name='connect_with_user'),
    path('projects/<int:student_pk>', my_projects, name='my_projects'),
    path('add/project/image/<int:project_pk>', add_project_image, name='add_project_image'),
    path('delete/project/<int:pk>', DeleteProjectView.as_view(), name='delete_project'),
    path('update/project/<pk>', UpdateProjectView.as_view(), name='update_project'),
    path('add/project/image/<int:project_pk>', add_project_image, name='add_project_image'),
    path('', index, name='index'),
    path('new/student/project', new_student_project, name='new_student_project'),
    path('project/<int:project_pk>', project_detail, name='project_detail'),
]
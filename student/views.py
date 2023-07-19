from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from accounts.models import Student
from .models import (
    ProjectImage, StudentProject
)
from studio.models import Project
from .forms import (
    StudentProjectForm, ProjectImageForm
)
from blog.models import Post, Comment
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth import get_user_model

User = get_user_model()

def index(request):
    username = request.user.username
    student = get_object_or_404(Student, username=username)
    student_projects = StudentProject.objects.all()
    posts = Post.objects.order_by('-created')[0:5]
    my_projects = student.student_projects.order_by('-name')
    other_students = Student.objects.exclude(pk=student.pk)
    my_network = student.network.all()
    return render(request, 'student/index.html', {
        'latest_projects': Project.objects.order_by('-created')[0:5],
        'posts': posts,
        'student_projects': student_projects,
        'my_projects': my_projects,
        'student': student,
        'other_students': other_students,
        'my_network': my_network
    })

@login_required
def new_student_project(request):
    if  request.user.is_student:
        username = request.user.username
        student = Student.objects.get(username=username)    
        if request.method == 'POST':
            form = StudentProjectForm(request.POST, request.FILES)
            if form.is_valid():
                project = form.save(commit=False)
                project.owner = student
                project.save()
                return redirect('student:project_detail', project.pk)
        else:
            form = StudentProjectForm()
        return render(request, 'student/forms/project_form.html', {
            'form': form,
            'form_header': 'Create A New Project'

        })
    else: 
        return redirect('accounts:profile')
    

def project_detail(request, project_pk):
    project = get_object_or_404(StudentProject, pk=project_pk)
    return render(request, 'student/project_detail.html', {
        'project': project
    })

def add_project_image(request, project_pk):
    project = get_object_or_404(StudentProject, pk=project_pk)
    if request.method == 'POST': 
        form = ProjectImageForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user.is_student:
                image = form.save()
                project.project_images.add(image)
                return redirect('student:project_detail', project.pk)
            else:
                return redirect('home:index')
    else:
        form = ProjectImageForm()
    return render('student/forms/project_image_form.html', {
        'form': form,
        'project': project
    })

class UpdateProjectView(UpdateView):
    model = StudentProject
    template_name = 'student/forms/studentproject_update_form.html'
    success_url = '/student'
    fields = ['name', 'intro', 'description', 'image', 'tags']



class DeleteProjectView(DeleteView):
    model = StudentProject
    success_url = reverse_lazy('student:index')
    template_name = 'student/forms/project_confirm_delete.html'

def add_project_image(request, project_pk):
    project = get_object_or_404(StudentProject, pk=project_pk)
    if request.method == 'POST':
        form = ProjectImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = image = form.save(commit=False)
            image.project = project
            image.save()
            project.images.add(image)
            return redirect('student:project_detail', project.pk)
    else:
        form = ProjectImageForm()
    return render(request, 'student/forms/project_image_form.html', {
        'project': project,
        'form': form
    })

def my_projects(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    my_projects = student.student_projects.order_by('-created')
    return render(request, 'student/my_projects.html', {
        'my_projects': my_projects,
        'student': student
    })

def connect_with_user(request, user_pk):
    this_username = request.user.username
    this_student = get_object_or_404(Student, username=this_username)
    other_student = get_object_or_404(User, pk=user_pk)
    this_student.network.add(other_student)
    return redirect('student:index')
    
    
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import (
    Category, ProjectImage, Project, Review, MainCategory,
)

from accounts.models import Designer, Moderator
from .forms import (
    CategoryForm, ProjectForm, ProjectImageForm, ReviewForm,
    MainCategoryForm
)
from blog.models import (
    Post
    )
from shop.models import (Product, ProductCategory, ProductImage)
from taggit.models import Tag
from django.contrib.auth.decorators import login_required, user_passes_test
from hitcount.views import HitCountDetailView
from django.views.generic import (
    DeleteView, UpdateView, DetailView
    )
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.mixins import (LoginRequiredMixin)

User = get_user_model()

def check_moderator(user):
    if user.is_moderator:
        return True
    else: 
        return False 


class ProjectMixinDetailView(object):
    model = Project
    
    def get_context_data(self, **kwargs):
        context = super(ProjectMixinDetailView, self).get_context_data(**kwargs)
        context['projects'] = Project.objects.order_by('-created')
        context['post_views'] = ["ajax", "detail", "detail-with-count"]
        context['categories'] = Category.objects.order_by('name')
        return context

class ProjectDetailView(ProjectMixinDetailView, HitCountDetailView):
    
    count_hit = True        

@login_required(login_url='/accounts/login')
@user_passes_test(check_moderator)
def moderator(request):
    if request.user.is_moderator:
        categories = Category.objects.prefetch_related(
            'project.id').order_by('-name')
        projects = Project.objects.order_by('-created')
        blog_posts = Post.objects.prefetch_related(
            'author').order_by('-created')
        users = User.objects.order_by('-last_name')
        return render(request, 'studio/moderator/dashboard.html', {
            'categories': categories,
            'blog_posts': blog_posts,
            'projects': projects,
            'users': users,

        })
    else:
        return redirect('accounts:login')


@login_required(login_url='/accounts/login')
def designer(request):
    if request.user.is_designer:
        categories = Category.objects.prefetch_related('project').order_by('-name')
        projects = Project.objects.order_by('-created')
        blog_posts = Post.objects.prefetch_related('author').order_by('-created')
        return render(request, 'studio/designer/dashboard.html', {
           'categories': categories,
           'blog_posts': blog_posts,
           'projects': projects,

        })
    else:
        return redirect('accounts:login')


@login_required(login_url='/accounts/login')
def index(request):
    users = User.objects.all()
    posts = Post.objects.order_by('-created')
    projects = Project.objects.order_by('-name')
    latest_projects = Project.objects.all()[0:5]
    return render(request, 'studio/index.html', {
        'users': users,
        'posts':posts,
        'projects': projects,
        'latest_projects': latest_projects,
        'products': Product.objects.order_by('-name') 
    })


@login_required(login_url='/accounts/login')
def project_categories(request):
    categories = Category.objects.order_by('-name')
    return render(request, 'studio/project_categories.html', {
        'categories': categories
    })


@login_required(login_url='/accounts/login')
def new_project(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.category = category
            project.owner = request.user
            project.save()
            form.save_m2m()
            return redirect('studio:project_detail', project.pk)
    else:
        form = ProjectForm()
    return render(request, 'studio/forms/project_form.html', {
        'form': form,
        'form_title': 'Set Up A New Project in {}'.format((category.name))
    })


@login_required(login_url='/accounts/login')
def review_project(request, project_pk):
    categories = Category.objects.all()
    project = get_object_or_404(Project, pk=project_pk)
    category = project.category
    common_tags = project.tags.most_common()[0:4]
    reviews = project.reviews.order_by('-created')
    related_projects = Project.objects.exclude(pk=project.pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.project = project
            review.save()
            return redirect('studio:project_detail', project.pk)
    else:
        form = ReviewForm()
    return render(request, 'studio/review_project.html', {
        'project': project,
        'review_form': form,
        'form_title': 'Review {}`s project'.format(project.owner.get_full_name()),
        'reviews': reviews,
        'related_projects': related_projects,
        'categories': categories,

    })


@login_required(login_url='/accounts/login')
def main_category_detail(request, main_category_pk):
    main_category = get_object_or_404(MainCategory, pk=main_category_pk)
    other_categories = MainCategory.objects.exclude(pk=main_category.pk)
    return render(request, 'studio/main_category_detail.html', {
        'main_category': main_category,
        'other_categories': other_categories
    })



def category_detail(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    other_categories = Category.objects.exclude(pk=category.pk)
    return render(request, 'studio/category_detail.html', {
        'category': category,
        'other_categories': other_categories
    })



def projects(request):
    projects = Project.objects.order_by('-name')
    return render(request, 'studio/projects.html', {
        'projects': projects
    })



def project_tags(request, tag):
    projects = Project.objects.filter(tags__name=tag)
    return render(request, 'studio/tagged_projects.html', {
        'projects': projects,
        'tag': tag
    })


@login_required(login_url='/accounts/login')
def new_main_category(request):
    main_categories = MainCategory.objects.all()
    if request.method == 'POST':
        form = MainCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            main_category = form.save()
            return redirect('studio:main_category_detail', main_category.pk)
    else:
        form = MainCategoryForm()
    return render(request, 'studio/forms/main_category_form.html', {
        'form': form,
        'main_categories': main_categories
    })



def main_categories(request):
    main_categories = MainCategory.objects.order_by('-name')
    return render(request, 'studio/main_categories.html', {
        'main_categories': main_categories
    })


@login_required(login_url='/accounts/login')
def new_category(request, main_category_pk):
    main_category = get_object_or_404(MainCategory, pk=main_category_pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.main_category = main_category
            category.save()
            return redirect('studio:category_detail', category.pk)
    else:
        form = CategoryForm()
    return render(request, 'studio/forms/category_form.html', {
        'form': form,
        'form_title': 'Add a category to {}'.format(main_category.name)
    })


@login_required(login_url='/accounts/login')
def users(request):
    users = User.objects.order_by('-last_name')
    return render(request, 'studio/moderator/users.html', {
        'users': users
    })


@login_required(login_url='/accounts/login')
def user_detail(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    return render(request, 'studio/moderator/user_detail.html', {
        'user': user
    })


@login_required(login_url='/accounts/login')
def my_projects(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    my_projects = user.projects.order_by('-created')
    return render(request, 'studio/my_projects.html', {
        'user': user,
        'my_projects': my_projects
    })


class ProjectUpdateView(LoginRequiredMixin, UpdateView):

    model = Project
    template_name = 'studio/forms/update_project_form.html'
    fields = ['name', 'image', 'intro', 'video','description', 'tags']

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy('studio:my_projects', kwargs={'user_pk': user.pk})


class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'studio/forms/project_confirm_delete.html'

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy('studio:my_projects', kwargs={
            'user_pk': user.pk
        }) 


@login_required(login_url='/accounts/login')
def new_project_image(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.method == 'POST':
        form = ProjectImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            project.images.add(image)
            project.save()
            return redirect('studio:project_detail', project.pk)
    else:
        form = ProjectImageForm()
    return render(request, 'studio/forms/project_image_form.html', {
        'project': project,
        'form': form,
    })


def search_projects(request):
    projects = None
    query = request.GET.get('pq')
    if query is not None:
        projects = Project.objects.filter(Q(owner__last_name__icontains=query)|Q(owner__first_name__icontains=query)|Q(name__icontains=query))
    return render(request, 'studio/search_projects.html', {
        'projects': projects,
        'query': query
    })

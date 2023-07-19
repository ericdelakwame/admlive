from django.utils.safestring import SafeString
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import (
    ModeratorRequest, Profile, Task
)
from accounts.forms import TaskForm
from blog.models import (
    Post, PostImage, Comment, PostReply
)
from blog.forms import (
    PostForm, PostImageForm, PostReplyForm, CommentForm
)
from .tasks import caution_comment_author
from student.models import StudentProject

from studio.models import (
    Category, Project, ProjectImage, MainCategory,
)

from studio.forms import (
    CategoryForm, ProjectForm, ProjectImageForm, MainCategoryForm,

)
from orders.models import (
    Order, OrderItem
)

from shop.models import (
    Product, ProductCategory
)
from home.models import AboutImage, AboutNote, Resource
from .forms import (
    AboutImageForm, AboutNoteForm, PressNoteForm, ResourceForm
)
from django.db.models import (
    Sum, Max, Avg, Count, Aggregate
)
from django.views.generic import (
    UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from adm_slack.models import SlackChannel
User = get_user_model()

slack_token = settings.SLACK_AUTH_TOKEN 
slack_client_id = settings.SLACK_CLIENT_ID
import requests
import os
import logging
from time import time
from slack_sdk import WebClient
from adm_slack.models import SlackChannel
from adm_slack.forms import SlackChannelForm
from django.core.paginator import Paginator
from .models import PressNote


def new_press(request):
    if request.method == 'POST':
        form = PressNoteForm(request.POST,  request.FILES)
        if form.is_valid():
            press = form.save()
            return redirect('dashboard:press_detail',press.pk)
    else:
        form = PressNoteForm()
    return render(request, 'dashboard/forms/press_note_form.html', {
        'form': form
    }) 
    
def press_detail(request, press_pk):
    press = get_object_or_404(PressNote, pk=press_pk)
    return render(request, 'dashboard/press_detail.html', {
        'press': press
    })

# Resource


def new_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST,request.FILES)
        if form.is_valid():
            resource = form.save()
            return redirect('dashboard:resource_detail', resource.pk)
    else:
        form = ResourceForm()
    return render(request, 'dashboard/forms/resource_form.html', {
        'form': form
    })


def resource_detail(request, resource_pk):
    resource = get_object_or_404(Resource, pk=resource_pk)
    return render(request, 'dashboard/resource_detail.html', {
        'resource': resource
    })

class UpdateResourceView(LoginRequiredMixin, UpdateView):
    model = Resource
    template_name = 'dashboard/forms/resource_update_form.html'
    fields = ['content']
    
    def get_success_url(self, *args, **kwargs):
        pk = self.kwargs['pk']
        resource = get_object_or_404(Resource, pk=pk)
        return reverse_lazy('dashboard:resource_detail', kwargs={'resource_pk': pk})

class DeleteResourceView(LoginRequiredMixin, DeleteView):
    model = Resource
    success_url = '/dashboard/index'


class UpdatePressView(LoginRequiredMixin, UpdateView):
    model = PressNote
    template_name = 'dashboard/forms/press_update_form.html'
    fields = ['content']

    def get_success_url(self, *args, **kwargs):
        pk = self.kwargs['pk']
        press = get_object_or_404(Press, pk=pk)
        return reverse_lazy('dashboard:press_detail', kwargs={'press_pk': pk})


class DeletePressView(LoginRequiredMixin, DeleteView):
    model = PressNote
    success_url = '/dashboard/index'




def admin_pass(user):
    if user.is_superuser:
        return True
    else: 
        return False

@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def index(request):
    press_notes = PressNote.objects.all()
    resources = Resource.objects.all()
    # add_to_slack = "https://slack.com/oauth/authorize?scope=bot&client_id={}".format(
    #     slack_client_id)
    # client = WebClient(token=slack_token)
    # response = client.conversations_list()
    # slack_channels = response['channels']
    sold_list = []
    sold_data = {}
    products_sold = OrderItem.objects.values(
        'product__name').annotate(Max('quantity'))
    for i in products_sold:
        sold_data['product'] = i['product__name']
        sold_data['quantity'] = i['quantity__max']
        sold_list.append(sold_data)
    users = User.objects.all()
    projects = Project.objects.all()
    student_projects = StudentProject.objects.order_by('-created')
    moderators = User.objects.filter(is_moderator=True)
    posts = Post.objects.all()
    students = User.objects.filter(is_student=True)
    studios = User.objects.filter(is_designer=True)
    latest_projects = Project.objects.order_by('-created')[0:5]
    orders = Order.objects.order_by('-created')
    mod_requests = ModeratorRequest.objects.filter(accepted=False)
    blog_comments = Comment.objects.select_related(
        'post').order_by('-created')[0:9]
    products = Product.objects.all()
    product_categories = ProductCategory.objects.all()
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('accounts:profile')
    else:
        form = TaskForm()
    return render(request, 'dashboard/index.html',
                  {
                      'product_categories': product_categories,
                      'mod_requests': mod_requests,
                      'blog_comments': blog_comments,
                      'users': users,
                      'projects': projects,
                      'moderators': moderators,
                      'posts': posts,
                      'students': students,
                      'student_projects': student_projects,
                      'studios': studios,
                      'latest_projects': latest_projects,
                      'orders': orders,
                      'order_items': OrderItem.objects.order_by('-created'),
                      'products': products,
                      'sold_list': sold_list[0:2],
                      'task_form': form,
                      'tasks': Task.objects.order_by('due_date').filter(completed=False, user=request.user),
                      'press_notes': press_notes,
                      'resources': resources
                    #   'slack_btn': add_to_slack,
                    #   'slack_channels': slack_channels,
                    
                  })

def resources(request):
    resources = Resource.objects.all()
    return render(request, 'dashboard/resources.html', {
        'resources': resources
    })


def press_notes(request):
    press_notes = PressNote.objects.all()
    return render(request, 'dashboard/press_notes.html', {
        'press_notes': press_notes
    })


def ethnicity_view(request):
    e_data = []
    e_labels = []
    ethnicity_queryset = User.objects.values('ethnicity').exclude(ethnicity__exact='').annotate(e_count=Count('ethnicity'))
    for i in ethnicity_queryset:
        e_data.append(i['e_count'])
        e_labels.append(i['ethnicity'])
    return JsonResponse(data={'data':e_data, 'labels':e_labels})

def gender_view(request):
    gender_labels = []
    gender_data = []
    gender_queryset = User.objects.values('gender').exclude(gender__exact='').annotate(gender_count=Count('gender'))
    for i in gender_queryset:
        gender_labels.append(i['gender'])
        gender_data.append(i['gender_count'])
    return JsonResponse(data={'data': gender_data, 'labels': gender_labels})


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def users(request):
    users = User.objects.order_by('-last_name')
    return render(request, 'dashboard/users.html', {
        'users': users
    })


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def user_detail(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    return render(request, 'dashboard/user_detail.html', {'user': user})


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def new_project_category(request, topcat_pk):
    main_category = get_object_or_404(MainCategory, pk=topcat_pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.main_category = main_category
            category.save()
            return redirect('dashboard:category_detail', category.pk)
    else:
        form = CategoryForm()
    return render(request, 'dashboard/forms/project_category_form.html', {
        'form': form
    })


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def category_detail(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    return render(request, 'dashboard/category_detail.html', {
        'category': category
    })


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def review_mod_request(request, mod_request_pk):
    mod_request = get_object_or_404(ModeratorRequest, pk=mod_request_pk)
    return render(request, 'dashboard/review_mod_request.html', {
        'mod_request': mod_request
    })


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def accept_mod_request(request, mod_request_pk):
    mod_request = get_object_or_404(ModeratorRequest, pk=mod_request_pk)
    user = mod_request.user
    user.is_moderator = True
    user.save()
    return redirect('dashboard:user_detail', user.pk)


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def reject_mod_request(request, mod_request_pk):
    mod_request = get_object_or_404(ModeratorRequest, pk=mod_request_pk)
    user = mod_request.user
    user.is_moderator = False
    user.save()
    return redirect('dashboard:user_detail', user.pk)


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def activate_user(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    user.activated = True
    user.save()
    return redirect('dashboard:user_detail', user.pk)


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def deactivate_user(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    user.activated = False
    user.save()
    return redirect('dashboard:user_detail', user.pk)


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def projects(request):
    project_list = Project.objects.order_by('-created')
    paginator = Paginator(project_list, 10)
    page = request.GET.get('page')
    projects = paginator.get_page(page)
    return render(request, 'dashboard/projects.html', {
        'projects': projects
    })


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def new_main_category(request):
    main_categories = MainCategory.objects.all()
    if request.method == 'POST':
        form = MainCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            main_category = form.save()
            return redirect('dashboard:main_category_detail', main_category.pk)
    else:
        form = MainCategoryForm()
    return render(request, 'dashboard/forms/main_category_form.html', {
        'form': form,
        'main_categories': main_categories
    })


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def main_categories(request):
    main_categories = MainCategory.objects.order_by('-name')
    return render(request, 'dashboard/main_categories.html', {
        'main_categories': main_categories
    })


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def main_category_detail(request, topcat_pk):
    top_cat = get_object_or_404(MainCategory, pk=topcat_pk)
    return render(request, 'dashboard/main_category_detail.html', {
        'main_category': top_cat
    })


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def remove_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    post = comment.post
    caution_comment_author.delay(post.id)
    comment.delete()
    post.save()
    return redirect('dashboard:index')


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def publish_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    post = comment.post
    comment.publish = True
    comment.save()
    post.save()
    return redirect('dashboard:index')


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def new_post(request):
    previous_posts = Post.objects.order_by('-created')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if post.author.is_superuser:
                post.save()
                form.save_m2m()
                return redirect('dashboard:post_detail', post.pk)
            else:
                return redirect('accounts:profile')
    else:
        form = PostForm()
    return render(request, 'dashboard/forms/post_form.html', {
        'form': form,
        'form_title': 'New Post',
        'previous_posts': previous_posts,
    })


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def posts(request):
    posts = Post.objects.order_by('-created')
    return render(request, 'dashboard/posts.html', {
        'posts': posts
    }
    )


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comments = post.comments.order_by('-created').filter(publish=True)
    other_posts = Post.objects.exclude(pk=post.pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('dashboard:post_detail', post.pk)
    else:
        form = CommentForm()
        return render(request, 'dashboard/post_detail.html', {
            'comment_form': form,
            'post': post,
            'comments': comments,
            'other_posts': other_posts,

        })


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def post_images(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = PostImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            post.images.add(image)
            return redirect('dashboard:post_detail', post.pk)
    else:
        form = PostImageForm()
    return render(request, 'dashboard/forms/post_image_form.html', {
        'post': post,
        'form': form
    })


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def post_reply(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, publish=True)
    post = comment.post
    comments = post.comments.order_by('-created').filter(publish=True)
    replies = comment.replies.order_by('-created')
    if request.method == 'POST':
        reply_form = PostReplyForm(request.POST, request.FILES)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.comment = comment
            reply.author = request.user
            reply.save()
            return redirect('blog:post_detail', post.pk)
    else:
        reply_form = PostReplyForm()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comment': comment,
        'comments': comments,
        'replies': replies,
        'reply_form': reply_form

    })


class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['heading', 'subheading', 'intro', 'content', 'image']
    template_name = 'dashboard/forms/post_update_form.html'

    def get_success_url(self, **kwargs):
        pk= self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        return reverse_lazy('dashboard:post_detail',kwargs={'post_pk':pk})


@login_required(login_url='/accounts/login')
def categories(request):
    categories = Category.objects.order_by('name')
    return render(request, 'dashboard/categories.html', {
        'categories': categories
    })


class UpdateCategoryView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name', 'category_info', 'image']
    template_name = 'dashboard/forms/category_update_form.html'

    def get_success_url(self, **kwargs):
        pk = self.kwargs['pk']
        category = Category.objects.get(pk=pk)
        return reverse_lazy('dashboard:category_detail', kwargs={'category_pk': pk})




class DeletePostView(DeleteView):
    model = Post
    success_url = '/dashboard/'
    template_name = 'dashboard/post_confirm_delete.html'


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def remove_task(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    task.delete()
    return redirect('dashboard:index')


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def enable_paragon(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    user.is_paragon = True
    user.save()
    return redirect('dashboard:user_detail', user.pk)


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def enable_moderator(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    user.is_designer = False
    user.is_moderator = True
    user.save()
    return redirect('dashboard:user_detail', user.pk)


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def disable_moderator(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    user.is_designer = True
    user.is_moderator = False
    user.save()
    return redirect('dashboard:user_detail', user.pk)


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def publish_all_comments(request):
    unpublished_comments = Comment.objects.filter(publish=False)
    for comment in unpublished_comments:
        comment.publish = True
        comment.save()
    return redirect('dashboard:index')


def slack(request):
    return render(request, 'dashboard/slack.html', {

    })

def list_slack_channels(request):
    client = WebClient(token=slack_token)
    response = client.conversations_list()
    conversations = response['channels']
    return render(request, 'dashboard/slack/list_channels.html', {
        'conversations': conversations
    })


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def create_channel(request):
    client = WebClient(token=slack_token)
    if request.method == 'POST':
        form = SlackChannelForm(request.POST)
        if form.is_valid():
            new_channel = form.save()
            channel_name = new_channel.name
            response = client.conversations_create(name=channel_name, is_private=True)
            channel_id = response['channel']['id']
            response = client.conversations_archive(channel=channel_id)
            return redirect('dashboard:list_slack_channels')
    else:
        form = SlackChannelForm()
    return render(request, 'dashboard/forms/slack_channel_form.html', {
        'form': form
    })


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def add_about_note(request):
    if request.method == 'POST':
        form = AboutNoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save()
            return redirect('dashboard:about_note_detail', note.pk)
    else:
        form = AboutNoteForm()
    return render(request, 'dashboard/forms/about_note_form.html', {
        'form': form
    })


@login_required(login_url='/accounts/login')
@user_passes_test(admin_pass)
def about_note_detail(request, about_pk):
    about_note = get_object_or_404(AboutNote, pk=about_pk)
    return render(request, 'dashboard/about_note_detail.html', {
        'about_note': about_note
    })

from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    Post, Comment, PostImage, PostReply
)
from .forms import (
    PostForm, PostReplyForm, CommentForm, PostImageForm
)
from studio.models import Category
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def posts(request):
    post_list = Post.objects.order_by('-created')
    paginator = Paginator(post_list, 10)
    page = request.GET.get(paginator)
    posts = paginator.get_page(post_list)
    return render(request, 'blog/posts.html', {
        'posts': posts
    })


@login_required(login_url='/accounts/login')
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('blog:post_detail', post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/forms/post_form.html', {
        'form': form,
        'form_title': 'New Post'
    })


@login_required(login_url='/accounts/login')
def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comments = post.comments.order_by('-created')
    categories = Category.objects.order_by('name')
    other_posts = Post.objects.exclude(pk=post.pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', post.pk)
    else:
        form = CommentForm()
        return render(request, 'blog/post_detail.html', {
            'comment_form': form,
            'post': post,
            'comments': comments,
            'other_posts': other_posts,
            'categories': categories
        })


@login_required(login_url='/accounts/login')
def post_images(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = PostImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            post.images.add(image)
            return redirect('blog:post_detail', post.pk)
    else:
        return render(request, 'blog:post_detail', post.pk, {
            'post': post,
            'image_form': form
        })

@login_required(login_url='/accounts/login')
def post_reply(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, publish=True)
    post = comment.post
    comments = post.comments.order_by('-created')
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

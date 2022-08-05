from datetime import date, datetime
from sre_parse import CATEGORIES
from traceback import print_tb
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import is_valid_path, reverse
from .models import Category, Post, Comment
from .forms import NewPostForm, NewCommentForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.views.generic import UpdateView, ListView, CreateView,DeleteView
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from urllib import request
from django.core.mail import send_mail
from better_profanity import profanity

# Create your views here.

def home(req):
    categories = Category.objects.all()
    posts = Post.objects.all().order_by('-created_dt')
    return render(req, 'categories/home.html', {'categories': categories, "posts": posts})


def homeTags(req, tag_slug):
    categories = Category.objects.all()
    posts = Post.objects.filter(tags__slug=tag_slug).order_by('-created_dt')
    return render(req, 'categories/home.html', {'categories': categories, "posts": posts})


def searchPosts(req):
    categories = Category.objects.all()
    posts = Post.objects.filter(
        title__contains=req.POST['search']).order_by('-created_dt')
    return render(req, 'categories/home.html', {'categories': categories, "posts": posts})


def new_category(req):
    if req.method == 'POST':
        name = req.POST['name']

        category = Category.objects.create(
            name=name
        )
        return redirect('home')
    return render(req, 'categories/new_category.html')


def category_posts(req, category_id):
    category = get_object_or_404(Category, pk=category_id)
    # posts = Post.objects.all().order_by('-created_dt')
    posts = category.posts.all().order_by('-created_dt')
    # return render(req, 'categories/posts.html', {'category': category})
    return render(req, 'categories/posts.html', {'posts': posts, 'category': category})


@login_required
def new_post(req, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if req.method == "POST":
        form = NewPostForm(req.POST)
        if form.is_valid():
            # title and content of post is auto graped and saved by postform
            post = form.save(commit=False)
            # here added extra data to be saved with post
            post.category = category
            post.created_by = req.user
            try:
                post.image = f"imgs/{req.FILES['image']}"
                image = req.FILES["image"]
                fss = FileSystemStorage()
                fss.save(f"imgs/{image.name}", image)
            except:
                post.image = "imgs/blank.png"

            post.save()
            form.save_m2m()
            return redirect('category_posts', category_id=category.pk)
    else:
        form = NewPostForm()

    return render(req, 'categories/new_post.html', {'category': category, 'form': form})


@login_required
def post(req, category_id, post_id):
    post = get_object_or_404(Post, category__pk=category_id, pk=post_id)
    categories=Category.objects.all()
    
    if req.method == 'POST':
        form = NewCommentForm(req.POST)
        if form.is_valid():

            comment = form.save(commit=False)
            comment.created_by = req.user
            comment.post = post
            comment.save()
            return redirect('post', category_id=category_id, post_id=post_id)

    else:
        form = NewCommentForm()

    return render(req, 'categories/post.html', {'post': post, 'form': form, 'categories': categories})


# like_dislike
def like_post(req, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if req.user in post.like.all():
        return redirect('post', category_id=post.category.id, post_id=post.id)
    else:
        post.like.add(req.user)
        if req.user in post.dislike.all():
            post.dislike.remove(req.user)
    return redirect('post', category_id=post.category.id, post_id=post.id)


def dislike_post(req, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if req.user in post.dislike.all():
        return redirect('post', category_id=post.category.id, post_id=post.id)
    else:
        post.dislike.add(req.user)
        if req.user in post.like.all():
            post.like.remove(req.user)
        if post.dislike.all().count() == 4:
            print("post deleted")
            post.delete()
            return redirect('category_posts', category_id=post.category.id)
    return redirect('post', category_id=post.category.id, post_id=post.id)


class PostEdit(UpdateView):
    model = Post
    fields = ('title', 'content', "tags", 'category')
    template_name = 'categories/editPost.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_dt = timezone.now()
        post.save()
        form.save_m2m()
        return redirect('post', category_id=post.category.id, post_id=post.id)


def subscribe_unsubscribe(req, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if req.user in category.subscribe.all():
        category.subscribe.remove(req.user)
    else:
        category.subscribe.add(req.user)
        mess = 'hello ' + req.user.first_name + ' You have subscribed successfully in ' + category.name
        send_mail('confirm subscription',mess,'admin',[req.user.email])
        print("email sent")
    return redirect(reverse('home'))

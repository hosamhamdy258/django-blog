from traceback import print_tb
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import is_valid_path
from .models import Category, Post, Comment
from .forms import NewPostForm, NewCommentForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.views.generic import UpdateView
from django.utils import timezone


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
    posts = Post.objects.filter(title__contains=req.POST['search']).order_by('-created_dt')
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
    return render(req, 'categories/posts.html', {'category': category})


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

    return render(req, 'categories/post.html', {'post': post, 'form': form})


class PostEdit(UpdateView):
    model = Post
    fields = ('title', 'content',"tags")
    template_name = 'categories/editPost.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_dt = timezone.now()
        post.save()
        form.save_m2m()
        return redirect('post',category_id=post.category.id,post_id=post.id)

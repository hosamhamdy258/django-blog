from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.urls import reverse
from .form import SignupForm
from django.views.generic import UpdateView, ListView, CreateView, DeleteView
from categories.models import Category, Post, Comment
from django.utils import timezone
import ast
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

# Create your views here.


def signUp(req):
    form = SignupForm()
    if req.method == "POST":
        form = SignupForm(req.POST)
        if form.is_valid():
            user = form.save()
            auth_login(req, user)
            return redirect('home')

    return render(req, 'accounts/signup.html', {'form': form})


def block_unblock(req, user_id):
    users = User.objects.all()
    user = get_object_or_404(User, pk=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()
    return render(req, 'accounts/block.html', {'user': user, 'users': users})


class PostEditAdmin(UpdateView):
    model = Post
    fields = ('title', 'content', "tags", "category")
    template_name = 'admin/edit_template.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_dt = timezone.now()
        post.save()
        form.save_m2m()
        return redirect('all_posts')


class CategoryEdit(UpdateView):
    model = Category
    fields = ('name',)
    template_name = 'admin/edit_template.html'
    pk_url_kwarg = 'category_id'
    context_object_name = 'category'

    def form_valid(self, form):
        form.save()
        return redirect('all_categorys')


class CommentEdit(UpdateView):
    model = Comment
    fields = ('massage', 'post',)
    template_name = 'admin/edit_template.html'
    pk_url_kwarg = 'comment_id'
    context_object_name = 'comment'

    def form_valid(self, form):
        form.save()
        return redirect('all_comments')


@method_decorator(staff_member_required, name='dispatch')
class AdminView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'admin/adminpanal.html'


class AdminPostsView(ListView):
    queryset = Post.objects.all().order_by('id')
    context_object_name = 'posts'
    template_name = 'admin/allposts.html'


class AdminCategorysView(ListView):
    queryset = Category.objects.all().order_by('id')
    context_object_name = 'categorys'
    template_name = 'admin/allcategorys.html'


class AdminCommentsView(ListView):
    queryset = Comment.objects.all().order_by('id')
    context_object_name = 'comments'
    template_name = 'admin/allcomments.html'


class AdminUsersView(ListView):
    queryset = User.objects.all().order_by('id')
    context_object_name = 'users'
    template_name = 'admin/users.html'

    def post(self, request):
        string_data = request.POST['clickeduser']
        res = ast.literal_eval(string_data)
        user = get_object_or_404(User, pk=res['user'])
        if res["action"] == "block":
            user.is_active = False
        else:
            user.is_active = True
        if res["action"] == "make_admin":
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False
        user.save()
        return redirect('all_users')


class AdminCommentAddView(CreateView):
    model = Comment
    context_object_name = 'comment'
    template_name = 'admin/edit_template.html'
    fields = ('massage', 'post')
    success_url = '/adminpanal/allcomments'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.created_by = self.request.user
        post.save()
        return redirect('all_comments')


class AdminCategoryAddView(CreateView):
    model = Category
    context_object_name = 'category'
    template_name = 'admin/edit_template.html'
    fields = "__all__"
    success_url = '/adminpanal/allcategorys'


class AdminPostAddView(CreateView):
    model = Post
    context_object_name = 'post'
    template_name = 'admin/edit_template.html'
    fields = ['title', 'content', 'tags', 'image', 'category', 'image']
    success_url = '/adminpanal/allposts'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.created_by = self.request.user
        post.updated_by = self.request.user
        post.updated_dt = timezone.now()
        try:
            post.image = f"imgs/{form.FILES['image']}"
            image = form.FILES["image"]
            fss = FileSystemStorage()
            fss.save(f"imgs/{image.name}", image)
        except:
            post.image = "imgs/blank.png"
        post.save()
        form.save_m2m()
        return redirect('all_posts')


class AdminCategoryDeleteView(DeleteView):
    model = Category
    template_name = 'admin/delete_template.html'
    pk_url_kwarg = 'category_id'
    success_url = '/adminpanal/allcategorys'


class AdminPostDeleteView(DeleteView):
    model = Post
    template_name = 'admin/delete_template.html'
    pk_url_kwarg = 'post_id'
    success_url = '/adminpanal/allposts'


class AdminCommentDeleteView(DeleteView):
    model = Comment
    template_name = 'admin/delete_template.html'
    pk_url_kwarg = 'comment_id'
    success_url = '/adminpanal/allcomments'

from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import Category, Post, Comment

admin.site.site_header = "Blog Panal"
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_by")
    list_filter = ("created_by", "category")
    search_fields = ("title",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "created_by",  "post", "massage")
    list_filter = ("created_by", "post")
    search_fields = ("post",)


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

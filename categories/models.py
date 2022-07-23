from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=4000, help_text="Max length is 4000")
    category = models.ForeignKey(
        Category, related_name='posts', on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        User, related_name='posts', on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="imgs", blank=True)
    tags = TaggableManager()
    updated_by=models.ForeignKey(User,null=True,related_name="update",on_delete=models.CASCADE)
    updated_dt=models.DateTimeField(null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    massage = models.TextField()
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)

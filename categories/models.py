import math
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    subscribe = models.ManyToManyField(User,null=True,blank=True)

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
    updated_by = models.ForeignKey(User, null=True, related_name="update", on_delete=models.CASCADE)
    updated_dt = models.DateTimeField(null=True)
    #like
    like = models.ManyToManyField(User, blank=True)
    dislike = models.ManyToManyField(User, blank=True,related_name="user_dislike")

    def num_likes(self):
        return self.like.all().count()

    def num_dislikes(self):
        return self.dislike.all().count()

    def __str__(self):
        return self.title

    def whenpublished(self):
        now = timezone.now()

        diff = now - self.created_dt

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days/30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"


class Comment(models.Model):
    # massage = models.TextField()
    massage = models.TextField()
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)

    def whenpublished(self):
        now = timezone.now()

        diff = now - self.created_dt

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days/30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

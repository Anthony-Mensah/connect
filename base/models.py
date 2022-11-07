from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_pic', null=True, blank=True)
    caption = models.TextField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    favorite = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.user.username + ' ' + self.caption

    class Meta:
        ordering = ['-created']

#COMMENTS
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.CharField(max_length=200)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.body[0:10]

    class Meta:
        ordering = ['-created']

# FOLLOW SYSTEM
class Follow(models.Model):
    followed = models.CharField(max_length=100, null=True)
    follower = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.follower + ' ' + 'follows' +  ' ' + self.followed

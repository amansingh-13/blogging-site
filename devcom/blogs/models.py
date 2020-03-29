from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_text = models.CharField(max_length=500)
    blog_title = models.CharField(max_length=40)
    datetime = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.blog_title


class Comment(models.Model):
    commentor = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=100)

    def __str__(self):
        return self.comment_text

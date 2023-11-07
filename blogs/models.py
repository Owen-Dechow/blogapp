from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Blog(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        to="BlogManager", on_delete=models.CASCADE, related_name="Blog_owner"
    )


class BlogManager(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="BlogManager_user"
    )
    blog = models.ForeignKey(
        to="Blog", on_delete=models.CASCADE, related_name="BlogManager_blog"
    )


class Post(models.Model):
    manager = models.ForeignKey(
        to="BlogManager", on_delete=models.CASCADE, related_name="Post_manager"
    )
    blog = models.ForeignKey(
        to="Blog", on_delete=models.CASCADE, related_name="Post_blog"
    )
    content = models.CharField(max_length=100)


class Comment(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="Comment_user"
    )
    blog = models.ForeignKey(
        to="Blog", on_delete=models.CASCADE, related_name="Comment_blog"
    )
    parent = models.ForeignKey(
        to="Comment", null=True, on_delete=models.CASCADE, related_name="Comment_parent"
    )


class CommentFlag(models.Model):
    comment = models.ForeignKey(
        to="Comment", on_delete=models.CASCADE, related_name="CommentFlag_comment"
    )
    manager = models.ForeignKey(
        to="BlogManager", on_delete=models.CASCADE, related_name="CommentFlag_manager"
    )
    reason = models.CharField(max_length=100)


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="Subscription_user"
    )
    blog = models.ForeignKey(
        to="Blog", on_delete=models.CASCADE, related_name="Subscription_blog"
    )


class Notification(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="Notification_user"
    )
    content = models.CharField(max_length=100)

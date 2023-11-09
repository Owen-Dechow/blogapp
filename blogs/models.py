from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Blog(models.Model):
    __str__ = lambda self: self.name

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        to="BlogManager",
        on_delete=models.CASCADE,
        related_name="Blog_owner",
        blank=True,
        null=True,
    )


class BlogManager(models.Model):
    __str__ = lambda self: f"{self.user} - {self.blog}"

    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="BlogManager_user"
    )
    blog = models.ForeignKey(
        to="Blog", on_delete=models.CASCADE, related_name="BlogManager_blog"
    )


class Post(models.Model):
    __str__ = lambda self: self.name

    manager = models.ForeignKey(
        to="BlogManager", on_delete=models.CASCADE, related_name="Post_manager"
    )
    blog = models.ForeignKey(
        to="Blog", on_delete=models.CASCADE, related_name="Post_blog"
    )

    name = models.CharField(max_length=100)
    content = models.CharField(max_length=100)


class Comment(models.Model):
    __str__ = (
        lambda self: f"*{self.user} - {self.parent}"
        if self.parent
        else f"{self.user} - {self.post}"
    )

    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="Comment_user"
    )
    post = models.ForeignKey(
        to="Post", on_delete=models.CASCADE, related_name="Comment_post"
    )
    parent = models.ForeignKey(
        to="Comment",
        null=True,
        on_delete=models.CASCADE,
        related_name="Comment_parent",
        blank=True,
    )

    date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=100)

    class Meta:
        ordering = ["-date"]


class CommentFlag(models.Model):
    __str__ = lambda self: f"{self.manager} - {self.comment}"

    comment = models.ForeignKey(
        to="Comment", on_delete=models.CASCADE, related_name="CommentFlag_comment"
    )
    manager = models.ForeignKey(
        to="BlogManager", on_delete=models.CASCADE, related_name="CommentFlag_manager"
    )
    reason = models.CharField(max_length=100)


class Subscription(models.Model):
    __str__ = lambda self: f"{self.user} - {self.blog}"

    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="Subscription_user"
    )
    blog = models.ForeignKey(
        to="Blog", on_delete=models.CASCADE, related_name="Subscription_blog"
    )


class Notification(models.Model):
    __str__ = lambda self: f"{self.user} Notification"

    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="Notification_user"
    )
    content = models.CharField(max_length=100)

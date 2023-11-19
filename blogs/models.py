from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Blog(models.Model):
    __str__ = lambda self: self.name

    name = models.CharField(max_length=100, unique=True)
    header = models.CharField(max_length=100, unique=True)

    owner = models.ForeignKey(
        to="BlogManager",
        on_delete=models.CASCADE,
        related_name="Blog_owner",
        blank=True,
        null=True,
    )

    @staticmethod
    def get_real_name(name: str):
        url_name = ""
        for l in name:
            if l.isalpha() or l.isdigit():
                url_name += l

    def save(self, *args, **kwargs):
        self.url_name = self.get_real_name(self.header)
        super().save(*args, **kwargs)


class BlogManager(models.Model):
    __str__ = lambda self: f"{self.user} - {self.blog}"

    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="BlogManager_user"
    )
    blog = models.ForeignKey(
        to="Blog", on_delete=models.CASCADE, related_name="BlogManager_blog"
    )


class Post(models.Model):
    __str__ = lambda self: self.name if self.name else f"post #: {self.id}"

    manager = models.ForeignKey(
        to="BlogManager", on_delete=models.CASCADE, related_name="Post_manager"
    )
    blog = models.ForeignKey(
        to="Blog", on_delete=models.CASCADE, related_name="Post_blog"
    )

    name = models.CharField(max_length=100)
    content = models.TextField()

    @classmethod
    def create_from_blog_manager(cls, blog_manager: BlogManager, blog: Blog):
        post = cls()
        post.manager = blog_manager
        post.blog = blog

        return post


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

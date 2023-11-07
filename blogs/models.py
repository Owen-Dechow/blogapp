from django.db import models


# Create your models here.
class Blog(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(to="BlogManager")


class BlogManager(models.Model):
    user = models.ForeignKey(to="User")
    blog = models.ForeignKey(to="Blog")


class Post(models.Model):
    manager = models.ForeignKey(to="BlogManager")
    blog = models.ForeignKey(to="Blog")
    content = models.CharField(max_length=100)


class Comment(models.Model):
    user = models.ForeignKey(to="User")
    blog = models.ForeignKey(to="Blog")
    parent = models.ForeignKey(to="Comment", null=True)


class CommentFlag(models.Model):
    comment = models.ForeignKey(to="Comment")
    manager = models.ForeignKey(to="BlogManager")
    reason = models.CharField(max_length=100)


class Subscription(models.Model):
    user = models.ForeignKey(to="User")
    blog = models.ForeignKey(to="Blog")


class Notification(models.Model):
    user = models.ForeignKey(to="User")
    content = models.CharField(max_length=100)

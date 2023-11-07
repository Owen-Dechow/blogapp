from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Blog)
admin.site.register(models.BlogManager)
admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.CommentFlag)
admin.site.register(models.Subscription)

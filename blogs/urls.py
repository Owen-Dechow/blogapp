from django.urls import path
from . import views


urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("blog/<int:blog_id>", views.blog, name="blog"),
    path("post/<int:post_id>", views.post, name="post"),
    path("comment", views.comment, name="comment"),
    path("get-replies", views.replies, name="get-replies"),
    path("get-comments", views.comments, name="get-comments"),
]

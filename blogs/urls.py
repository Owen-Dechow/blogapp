from django.urls import path
from . import views


urlpatterns = [
    path("", views.landing_page, name="landing-page"),
    path("blog/<int:blog_id>", views.blog, name="blog"),
    path("blog/<int:blog_id>/new-post", views.new_post, name="new-post"),
    path("post/<int:post_id>", views.post, name="post"),
    path("comment", views.comment, name="comment"),
    path("get-replies", views.replies, name="get-replies"),
    path("get-comments", views.comments, name="get-comments"),
    path("save-post", views.save_post, name="save-post"),
]

from django.urls import path
import django.contrib.auth.views as a_views
from . import views


blogspatterns = [
    path("", views.landing_page, name="landing-page"),
    path("b/<str:blog_name>/", views.blog, name="blog"),
    path("b/<str:blog_name>/<int:post_id>/", views.post, name="post"),
    path("b/<str:blog_name>/edit-post/", views.edit_post, name="edit_post"),
    path(
        "b/<str:blog_name>/edit-post/<int:post_id>/", views.edit_post, name="edit_post"
    ),
    path("comment/", views.comment, name="comment"),
    path("get-replies/", views.replies, name="get_replies"),
    path("get-comments/", views.comments, name="get_comments"),
    path("save-post/", views.save_post, name="save_post"),
    path("u/<str:username>/", views.user, name="user"),
    path("flag-comment/<int:comment_id>", views.flag_comment, name="flag_comment"),
]

authpatterns = [
    path(
        "accounts/login/",
        a_views.LoginView.as_view(
            template_name="accounts/login.html",
        ),
        name="login",
    ),
    path("accounts/logout/", a_views.LogoutView.as_view(), name="logout"),
    path("accounts/create_account/", views.create_account, name="create_account"),
    path("accounts/profile/", views.profile, name="profile"),
    path(
        "accounts/password_change/",
        a_views.PasswordChangeView.as_view(
            template_name="accounts/password_change.html",
        ),
        name="password_change",
    ),
    path(
        "accounts/password_change/done/",
        a_views.PasswordChangeDoneView.as_view(template_name="password_change_done"),
        name="password_change_done",
    ),
    path(
        "accounts/password_reset/",
        a_views.PasswordResetView.as_view(template_name="password_reset"),
        name="password_reset",
    ),
    path(
        "accounts/password_reset/done/",
        a_views.PasswordResetDoneView.as_view(template_name="password_reset_done"),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        a_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm",
        ),
        name="password_reset_confirm",
    ),
    path(
        "accounts/reset/done/",
        a_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete",
        ),
        name="password_reset_complete",
    ),
]

urlpatterns = blogspatterns + authpatterns

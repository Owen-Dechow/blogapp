from django.shortcuts import render, get_object_or_404, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from . import models
from . import forms
from . import clean_html

# Create your views here.
COMMENT_LOAD_COUNT = 10


def create_account(request: WSGIRequest):
    if request.method == "GET":
        form = forms.RegistrationForm()
    else:
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect("/accounts/profile/")

    return render(request, "accounts/create_account.html", {"form": form})


def profile(request: WSGIRequest):
    return render(request, "accounts/profile.html")


def landing_page(request: WSGIRequest):
    context = {
        "blog_list": models.Blog.objects.all(),
    }

    return render(request, "landing_page.html", context)


def blog(request: WSGIRequest, blog_name: str):
    blog = get_object_or_404(models.Blog, name=blog_name)
    context = {
        "blog": blog,
        "posts": models.Post.objects.filter(blog=blog),
    }

    return render(request, "blog.html", context)


def post(request: WSGIRequest, blog_name: str, post_id: int):
    try:
        post = models.Post.objects.select_related("blog", "manager").get(id=post_id)
    except ObjectDoesNotExist as e:
        raise Http404(e)

    comment_count = models.Comment.objects.filter(post=post_id, parent=None).count()
    comment_list = (
        models.Comment.objects.filter(post=post_id, parent=None)
        .order_by("-date")[:COMMENT_LOAD_COUNT]
        .annotate(replies=Count("Comment_parent"))
    )
    remaining_comments = comment_count - len(comment_list)

    context = {
        "post": post,
        "comment_list": comment_list,
        "comment_count": comment_count,
        "remaining_comments": remaining_comments,
        "number_of_loaded_comments": len(comment_list),
        "comment_form": forms.Comment(initial={"post": post.id}),
    }

    return render(request, "post.html", context)


@login_required
def comment(request: WSGIRequest):
    form = forms.Comment(request.POST)
    if form.is_valid():
        comment = form.save(request.user)
        return JsonResponse(
            {
                "success": True,
                "comment-id": comment.id,
            }
        )
    else:
        raise ValidationError("Form is invalid")


def replies(request: WSGIRequest):
    form = forms.ReplyRequest(request.GET)
    if form.is_valid():
        try:
            parent = int(form.cleaned_data["parent"])
            loaded = int(form.cleaned_data["loaded"])

            total = (
                models.Comment.objects.select_related("user")
                .filter(parent=parent)
                .count()
            )
            replies = models.Comment.objects.select_related("user").filter(
                parent=parent
            )[loaded : loaded + COMMENT_LOAD_COUNT]
        except ObjectDoesNotExist as e:
            raise Http404(e)

        objects = [{"user": x.user.username, "content": x.content} for x in replies]
        return JsonResponse(
            {
                "objects": objects,
                "loaded": loaded + len(objects),
                "remaining": total - loaded - len(objects),
            }
        )
    else:
        raise Http404("Invalid form")


def comments(request: WSGIRequest):
    form = forms.CommentRequest(request.GET)
    if form.is_valid():
        try:
            post = int(form.cleaned_data["post"])
            loaded = int(form.cleaned_data["loaded"])

            total = (
                models.Comment.objects.select_related("user")
                .filter(post=post, parent=None)
                .count()
            )
            comments = (
                models.Comment.objects.select_related("user")
                .filter(post=post, parent=None)
                .order_by("-date")[loaded : loaded + COMMENT_LOAD_COUNT]
                .annotate(replies=Count("Comment_parent"))
            )

        except ObjectDoesNotExist as e:
            raise Http404(e)

        objects = [
            {
                "user": x.user.username,
                "content": x.content,
                "replies": x.replies,
                "id": x.id,
            }
            for x in comments
        ]
        return JsonResponse(
            {
                "objects": objects,
                "loaded": loaded + len(objects),
                "remaining": total - loaded - len(objects),
            }
        )
    else:
        raise Http404("Invalid form")


@login_required
def edit_post(request: WSGIRequest, blog_name: str, post_id: int = -1):
    try:
        blog = models.Blog.objects.get(name=blog_name)
        manager = models.BlogManager.objects.select_related("blog").get(
            blog=blog, user=request.user
        )
    except ObjectDoesNotExist as e:
        raise Http404(e)

    if post_id == -1:
        content = ""
    else:
        post = get_object_or_404(models.Post, id=post_id)
        content = post.content

    context = {
        "blog": blog,
        "content": content,
        "post_id": post_id,
        "blog_name": blog_name,
    }

    return render(request, "edit_post.html", context)


@login_required
def save_post(request: WSGIRequest):
    form = forms.SavePost(request.POST)

    if not form.is_valid():
        raise Http404("Invalid save request")

    html = form.cleaned_data["content"]
    post_id = form.cleaned_data["post_id"]
    blog_name = form.cleaned_data["blog_name"]

    html = clean_html.clean_post(html)

    try:
        blog = models.Blog.objects.get(name=blog_name)
        manager = models.BlogManager.objects.select_related("blog").get(
            user=request.user, blog=blog
        )
    except ObjectDoesNotExist as e:
        raise Http404(e)

    if post_id == -1:
        post = models.Post.create_from_blog_manager(manager, blog)
    else:
        post = models.Post.objects.get(id=post_id)

    post.content = html
    post.save()

    return JsonResponse({"post-id": post.id})


def user(request: WSGIRequest, username: str):
    ...


def flag_comment(request: WSGIRequest, comment_id: str):
    ...

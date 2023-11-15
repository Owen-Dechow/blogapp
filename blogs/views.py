from django.shortcuts import render, get_object_or_404, Http404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from . import models
from . import forms
from bleach import clean, linkify, Cleaner
from bleach.css_sanitizer import CSSSanitizer
from bs4 import BeautifulSoup


# Create your views here.
COMMENT_LOAD_COUNT = 10


def landing_page(request: WSGIRequest):
    context = {
        "blog_list": models.Blog.objects.all(),
    }

    return render(request, "landing_page.html", context)


def blog(request: WSGIRequest, blog_id: int):
    context = {
        "blog": get_object_or_404(models.Blog, id=blog_id),
        "posts": models.Post.objects.filter(blog=blog_id),
    }

    return render(request, "blog.html", context)


def post(request: WSGIRequest, post_id: int):
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
def new_post(request: WSGIRequest, blog_id: int):
    try:
        manager = models.BlogManager.objects.select_related("blog").get(
            blog_id=blog_id, user=request.user
        )

        blog = manager.blog
    except ObjectDoesNotExist as e:
        raise Http404(e)

    context = {"blog": blog}

    return render(request, "new-post.html", context)


@login_required
def save_post(request: WSGIRequest):
    html = request.POST["content"]

    allowed_tags = [
        "a",
        "br",
        "p",
        "h1",
        "h2",
        "h3",
        "span",
        "code",
        "pre",
        "blockquote",
        "img",
        "li",
    ]

    allowed_attributes = {x: ["class", "style"] for x in allowed_tags}
    allowed_attributes["a"] += ["href", "target", "rel"]
    allowed_attributes["img"] += ["scr"]

    styles = [
        "color",
        "background-color",
    ]

    cleaner = Cleaner(
        tags=allowed_tags,
        attributes=allowed_attributes,
        css_sanitizer=CSSSanitizer(allowed_css_properties=styles),
    )

    html = cleaner.clean(html)
    html = linkify(html)

    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a"):
        a.attrs["target"] = "_blank"

    return HttpResponse(soup.contents)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]


class Comment(forms.Form):
    content = forms.CharField(
        max_length=models.Comment._meta.get_field("content").max_length,
        widget=forms.widgets.Textarea,
    )

    post = forms.IntegerField(widget=forms.widgets.HiddenInput)
    parent = forms.IntegerField(widget=forms.widgets.HiddenInput, required=False)

    def save(self, user):
        comment = models.Comment()
        comment.post_id = self.cleaned_data["post"]
        comment.parent_id = self.cleaned_data["parent"]
        comment.content = self.cleaned_data["content"]
        comment.user = user
        comment.save()
        return comment


class ReplyRequest(forms.Form):
    parent = forms.IntegerField()
    loaded = forms.IntegerField()


class CommentRequest(forms.Form):
    post = forms.IntegerField()
    loaded = forms.IntegerField()


class SavePost(forms.Form):
    post_id = forms.IntegerField()
    blog_name = forms.CharField(
        max_length=models.Blog._meta.get_field("name").max_length,
    )
    content = forms.CharField()
    post_name = forms.CharField(
        max_length=models.Post._meta.get_field("name").max_length
    )

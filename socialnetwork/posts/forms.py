from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    content = forms.CharField()

    class Meta:
        model = Post
        fields = ['content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text_body']

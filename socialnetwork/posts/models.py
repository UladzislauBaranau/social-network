from django.db import models
from django.utils.translation import gettext_lazy as _

from profiles.models import Profile


class Post(models.Model):
    content = models.TextField()
    post_author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    likes = models.ManyToManyField(Profile, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(Profile, blank=True, related_name='dislikes')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.post_author}: {self.content[:10]}"

    def n_comments(self):
        return self.comments.all().count()


class Comment(models.Model):
    text_body = models.TextField(default=_("Your comment..."), max_length=200)
    comment_author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.comment_author}: {self.text_body[:5]}"

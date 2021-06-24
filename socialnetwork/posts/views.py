from django.shortcuts import render

from .forms import PostForm
from .models import Post


def create_posts_view(request):
    qs_posts = Post.objects.all().filter(post_author=request.user)
    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.post_author = request.user
            new_post.save()

    context = {
        'form': form,
        'all_posts': qs_posts,
    }

    return render(request, 'posts/posts.html', context)

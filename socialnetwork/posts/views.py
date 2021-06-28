from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.edit import DeleteView, UpdateView

from profiles.models import Profile

from .forms import PostForm
from .models import Post


def create_posts_view(request):
    qs_posts = Post.objects.all().order_by('-date_created').filter(post_author=request.user)
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


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/edit_post.html'
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        profile = Profile.objects.get(id=self.request.user.id)
        if form.instance.post_author == profile:
            messages.success(self.request, _('A post has been updated'))
            return super().form_valid(form)
        else:
            super().form_invalid(form)
            messages.warning(self.request, _('You need to be the author of the post in to update it'))
            return redirect('posts')


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/remove_post.html'
    success_url = reverse_lazy('posts')

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if obj.post_author.id == self.request.user.id:
            messages.info(self.request, _('Your post has been deleted'))
            return super(DeletePostView, self).delete(request, *args, **kwargs)
        else:
            messages.warning(self.request, _('You need to be the author of the post to delete it'))
            return redirect('posts')

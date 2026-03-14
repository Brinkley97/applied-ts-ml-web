from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'feed/home.html', context)

# all posts
class PostListView(ListView):
    model = Post
    template_name = 'feed/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts' # same as above
    ordering = ['-date_posted'] # change order; newest first bc of "-" in front
    paginate_by = 7 # number of posts per page and have to open more; http://localhost:8000/?page=7, http://localhost:8000/?page=2, etc

# see all posts from specific user
class UserPostListView(ListView):
    model = Post
    template_name = 'feed/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 7

    # if user doesn't exists, 404
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

# single post
class PostDetailView(DetailView):
    model = Post

# create single post
# LoginRequiredMixin so user can't be logged out and can see a post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# update a post
# UserPassesTestMixin, so user that's updating a post is same as current/logged in user
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# delete a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' # home page, so http://localhost:8000/

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'feed/about.html', {'title': 'About'})
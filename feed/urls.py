from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='feed-home'), # 
    path('about/', views.about, name='feed-about'), 
]

from django.urls import path
from .views import (
    PostListView,
    UserPostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='feed-home'), # http://localhost:8000/feed/
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'), # http://localhost:8000/feed/
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), # http://localhost:8000/post/3/
    path('post/new/', PostCreateView.as_view(), name='post-create'), # http://localhost:8000/post/new/
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'), # http://localhost:8000/post/3/update/
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), # http://localhost:8000/post/3/delete/
    path('about/', views.about, name='feed-about'), # http://localhost:8000/feed/about
]
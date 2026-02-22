from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='feed-home'), # http://localhost:8000/feed/
    path('about/', views.about, name='feed-about'), # http://localhost:8000/feed/about
]
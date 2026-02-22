from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='feed-home'), # http://localhost:8000/feed/
]
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard_home/', views.home, name='dashboard-home'), # http://localhost:8000/dashboard_home/
]
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard_home/', views.home, name='dashboard-home'), # http://localhost:8000/dashboard_home/
    path('dashboard_home/forecast', views.forecast, name='dashboard-forecast'), # http://localhost:8000/dashboard_home/forecast
]
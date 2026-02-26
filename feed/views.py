from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

# when a user to to localhost:8000/home
def home(request):
    # return HttpResponse('<h1>Blog Home</h1>') 
    return render(request, 'feed/home.html')


def about(request):
    # return HttpResponse('<h1>About</h1>')
    return render(request, 'feed/about.html')
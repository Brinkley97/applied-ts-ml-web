from django.shortcuts import render
from .models import Post

# when a user to to localhost:8000/home
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 
                  'feed/home.html', 
                  context
                  )


def about(request):
    return render(request, 'feed/about.html', {'title': 'About'})
from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        'author': 'CoreyMS',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'August 28, 2018'
    }
]

# when a user to to localhost:8000/home
def home(request):
    return render(request, 
                  'feed/home.html', 
                  context = {'posts': posts}
                  )


def about(request):
    # return HttpResponse('<h1>About</h1>')
    return render(request, 'feed/about.html', {'title': 'About'})
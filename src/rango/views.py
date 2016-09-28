from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    title = 'Rango'
    context = {
        'title': title,
        'hello_message':'Rango says',
        'boldmessage': "Crunchy, creamy, cookies, candy, cupcake!"
    }
    return render(request, 'rango/index.html', context)

def about(request):
    title = 'About'
    context = {
        'title': title,
        'create_message' : 'This tutorial has been put together by'
    }

    return render(request, 'rango/about.html', context)

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'boldmessage': "Crunchy, creamy, cookies, candy, cupcake!"
    }
    return render(request, 'rango/index.html', context)

def about(request):
    return HttpResponse("Rango says here is the about page <a href='/rango/'> Home </a>")

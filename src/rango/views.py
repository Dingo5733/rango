from django.http import HttpResponse
from django.shortcuts import render

from rango.forms import CategoryForm
from rango.models import Category, Page

# Create your views here.
def index(request):
    # Query the database for a list of all categories stored
    # Order the categories by no. like in descending Order
    # Retrieve the Top 5 only, or all if less than 5
    # PLace the list in context
    # that will be passed to template engine

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    title = 'Rango'
    context = {
        'boldmessage': "Crunchy, creamy, cookies, candy, cupcake!",
        'categories': category_list,
        'pages': page_list,
        'hello_message':'Rango says',
        'title': title,
    }
    return render(request, 'rango/index.html', context)

def about(request):
    title = 'About'
    context = {
        'title': title,
        'create_message' : 'This tutorial has been put together by'
    }

    return render(request, 'rango/about.html', context)

def show_category(request, category_name_slug):
    # Create a context dictionary we can pass
    # to the template renering engine

    context = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises DoesNotExist exception
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)

        # retrieve all associated pages.
        # Note that filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)

        # Adds our results lists to the template context under name pages.
        context['pages'] = pages
        # we also add the category object
        # from the database to the context dictionary
        # We'll use this in the template to verify that the category exitsts
        context['category'] = category
    except Category.DoesNotExist:
        # we get here if we didnt find the specified category.
        # Don't do anything - the template will display the "no category"
        # message for us.
        context['category'] = None
        context['pages'] = None

    return render(request, 'rango/category.html', context)

def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)

    context = {
        'form': form,
    }

    return render(request, 'rango/add_category.html', context)

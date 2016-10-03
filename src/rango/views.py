
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)

from django.contrib.auth.decorators import (
    login_required,
)

from django.core.urlresolvers import(
    reverse,
)

from django.http import (
    HttpResponse,
    HttpResponseRedirect,
)

from django.shortcuts import(
    render
)

from rango.forms import (
    CategoryForm,
    PageForm,
    UserForm,
    UserProfileForm,
)

from rango.models import (
    Category,
    Page,
)

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

@login_required
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

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)

    except Category.DoesNotExist:
        category = None

    form = PageForm()

    if request.method == 'POST':
        form= PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

            return show_category(request, category_name_slug)
        else:
            print (form.errors)

    context = {
        'category': category,
        'form': form,
    }

    return render(request, 'rango/add_page.html', context)

def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value
    # to True when registration succeeds.

    #If it's a HTTP POST, we're interested in processing the
    # form data.

    registered = False

    if request.method == 'POST':
        #Attempt to grab the information frin the raw form information.
        # Note that we use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # save the user's form data to the database.
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model until
            # we're ready to avoid itegrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            #Did the user provide a profile picture?
            # If so, we need to get it from the input form
            # and put it in the UserProfile model.

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now save the UserProfile model instance.

            profile.save()

            #Update the variable to indicate that template
            # registration was successful.

            registered = True

        else:
            #Invalid form or forms - mistakes or something else?
            #Print problems to terminal
            print(user_form.errors, profile_form.errors)

    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank and ready for user input.

        user_form = UserForm()
        profile_form = UserProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
    }

    return render(request, 'rango/register.html', context )

def user_login(request):
    # If the request is a HTTP Post, try to pull the relevant information
    if request.method == 'POST':
        # Gather the username an password provided by user.
        # This information is obtained from the login form.
        # We use request.POST.get(<variable>) as opposed
        # to request .POST['<variable>'], because the
        # request.POST.get('<variabe>') returns None if the
        # value does not exist, while request.POST['<variabe>']
        # will raise a KeyError exception.

        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - A User object is returned if it is.

        user = authenticate(username=username, password=password)

        # IF we have a User object, the details are corrext.
        # If none (Python's way of representing th absence of a value),
        # no user with matching credits was found.

        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If thr account is activate, we can log the user in.
                # We'll send the user back to the home page.

                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                # an inactive account was used - no loggin in
                return HttpResponse('Your Rango account has been disabled')

        else:
            # a bad login
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

        # The request is not a HTTP POST, so display the login form.
        # This scenario would most likely be a HTTP GET.
    else:
        # No context variables pass to the template system, hence the
        # blank dictionary object.
        return render(request, 'rango/login.html', context=None)

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text.")

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just logged them out.
    logout(request)
    return HttpResponseRedirect(reverse('index'))

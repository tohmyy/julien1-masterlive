from django.http import HttpResponse
from django.shortcuts import redirect

from django.contrib.auth.models import Group, User
#decorator function
#if user is authenticated login redirects to homepage

def unauthenticated_user(view_func):#e.g. registerPage function replaces view_func here
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)#e.g. registerPage is return here

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None  #just a declared variable
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name #setting group variable as the name of the first user group
                print('current working role: ', group)
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page")
        return wrapper_func
    return decorator



def admin_Only(view_func):
    def wrapper_function(request, *args, **kwargs):

        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'admin':
            return view_func(request, *args, **kwargs)

        if group == 'customer':
            return redirect('user')
    return wrapper_function

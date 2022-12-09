from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):

    def wrapper_func(request, *args, **kwargs):

        if request.user.is_authenticated:

            return redirect("home")

        else:

            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):

    def decorator(view_func):

        def wrapper_func(request, *args, **kwargs):

            print("Working:", allowed_roles)
            print(request.user.groups)

            group = None

            if request.user.groups.exists():

                group = request.user.groups.all()[0].name
                print("🚀 ~ file: decorators.py:34 ~ group", group)

            if group in allowed_roles:

                return view_func(request, *args, **kwargs)

            else:

                return HttpResponse("You are not authorized to access this page")

        return wrapper_func

    return decorator

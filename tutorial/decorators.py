from collections import defaultdict
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Pacient, Tutore, User, PacientParsing


def restrict_unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('tutorial:website_index')
    return wrapper_func

def restrict_pacient_general_form(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        pacient = Pacient.objects.get(user = request.user)
        if pacient.flag == False:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('tutorial:website_index')
    return wrapper_func

def allowed_users(allowed_roles = []):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Nu esti autorizat sa vezi pagina asta !')
        return wrapper_func
    return decorator

def tutore_and_admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'tutore' or group == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('tutorial:website_index')
    return wrapper_func

def pacient_and_admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'pacient' or group == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('tutorial:website_index')
    return wrapper_func

def restrict_authenticated(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return redirect('tutorial:website_index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def restrict_pacient_mood(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        pacient = Pacient.objects.get(user = user)
        flag = pacient.flag
        if flag == False:
            return redirect('tutorial:website_index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def restrict_tutore_insert_patient(view_func):
    def wrapper_func(request, *args, **kwargs):
        username_get = request.user
        selected_user = Tutore.objects.get(user = username_get)

        print('!!!!!!!!!!!!')
        print(selected_user)
        print(selected_user.nr_pacienti)
        if selected_user.nr_pacienti > 100:
            return HttpResponse("Ne pare rau, ati introdus deja numarul maxim de pacienti !<br>"
                                "pentru a putea adauga mai multe persoane, va rugam consultati pachetele premium")
        return view_func(request, *args, **kwargs)
    return wrapper_func
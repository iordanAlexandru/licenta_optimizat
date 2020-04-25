from django.forms import forms
from django.http import HttpResponse

from .models import Pacient, Tutore, PacientParsing
from django.contrib.auth.models import Group

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .decorators import restrict_unauthenticated_user, restrict_tutore_patient, tutore_and_admin_only
from .forms import UserRegisterForm, PacientForm, GeneralForm, TutoreForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password




def index(request):
    return render(request, 'website/index.html')


def logoutPage(request):
    logout(request)
    return redirect('tutorial:website_index')


@restrict_unauthenticated_user
def about(request):
    return render(request, 'website/about.html', {'title': 'About'})


def registerPage(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        tf = TutoreForm(request.POST)
        if form.is_valid() and tf.is_valid():
            tf.cleaned_data['nr_pacienti'] = 0
            user = form.save()
            tutore = tf.save(commit = False)
            tutore.user = user
            tutore.save()
            group = Group.objects.get(name='tutore')
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('tutorial:website_loginPage')
    else:
        form = UserRegisterForm()
        tf = TutoreForm()
    return render(request, 'website/register.html', {'form': form, 'tut_form': tf})


def loginPage(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            if user.groups.filter(name='tutore').exists():
                t = Tutore.objects.get(user=request.user)
                if t.flag == False:
                    t.nr_pacienti = 0  # change field
                t.flag = True
                t.save()  # this will update only
            return redirect('tutorial:website_index')
        else:
            messages.info(request, 'userul sau parola este incorecta !')
    context = {}
    return render(request, 'website/login.html', context)


@restrict_unauthenticated_user
@tutore_and_admin_only
@restrict_tutore_patient
def pacient_create_view(request):
    if request.method == 'POST':
        form = PacientForm(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            pacientName = form.cleaned_data.get('prenume')
            if request.user.is_authenticated:
                fs.tutore = request.user.get_username()
                t = Tutore.objects.get(user = request.user)
                t.nr_pacienti += 1
                t.save()
            nume_pacient = form.cleaned_data['nume']
            prenume_pacient = form.cleaned_data['prenume']
            pass_pacient = form.cleaned_data['parola_pacient']
            fs.pass_pacient =  pass_pacient
            fs.user_pacient = nume_pacient.lower() + '.' + prenume_pacient.lower()

            fs.tutore = str(request.user)
            messages.success(request, f'Pacientul {pacientName} a fost inserat in sistem de catre {fs.tutore}')
            fs.save()
            user_pacient = User.objects.create_user(username=fs.user_pacient,password=fs.pass_pacient)
            group = Group.objects.get(name='pacient')
            user_pacient.groups.add(group)

            return redirect('tutorial:website_index')
    else:
        form = PacientForm()

    return render(request, 'website/update.html', {'form': form})


def pacient_general_form_view(request):
    if request.method == 'POST':
        form = GeneralForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.pacient = Pacient.objects.get(pk=1)
            form.rating = 100
            form.save()
            return redirect('tutorial:website_index')
    else:
        form = GeneralForm()
    return render(request, 'website/pacient_general_form.html', {'form': form})


def resultsView(request):
    all_entries = Pacient.objects.all()
    return render(request, 'website/results.html',{'all_entries': all_entries})

# form = PacientForm(request.POST)
# if form.is_valid():
#     form.save()
#     form = PacientForm()
# context = {
#     'form': form
# }
# return render(request, 'website/update.html', context)

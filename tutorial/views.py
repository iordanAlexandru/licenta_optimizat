from django.forms import forms
from django.http import HttpResponse

from .models import Pacient, Tutore, PacientParsing
from django.contrib.auth.models import Group

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .decorators import restrict_unauthenticated_user, restrict_tutore_patient, tutore_and_admin_only
from .forms import UserRegisterForm, PacientForm, GeneralForm, TutoreForm, AlzheimerForm, DiabetesForm,DementiaForm,DepressionForm
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
        if form.is_valid():
            user = form.save(commit = False)
            user.save()
            group = Group.objects.get(name='tutore')
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            Tutore.objects.create(user=user,nr_pacienti=0)
            messages.success(request, f'Account created for {username}!')
            return redirect('tutorial:website_loginPage')
    else:
        form = UserRegisterForm()
    return render(request, 'website/register.html', {'form': form})


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
        form_user = UserRegisterForm(request.POST)
        if form.is_valid() and form_user.is_valid():
            fu = form_user.save(commit=False)
            fs = form.save(commit=False)
            if request.user.is_authenticated:
                t = Tutore.objects.get(user = request.user)
                t.nr_pacienti += 1
                t.save()
            varsta = form.cleaned_data['varsta']
            afectiune = form.cleaned_data['afectiune']
            tel = form.cleaned_data['tel_urgenta']
            fu.save()
            fs.tutore = Tutore.objects.get(user = request.user)


            Pacient.objects.create(user=fu,
                                   varsta= varsta,
                                   afectiune=afectiune,
                                   tutore = fs.tutore,
                                   tel_urgenta= tel
                                   )

            group = Group.objects.get(name='pacient')
            fu.groups.add(group)
            return redirect('tutorial:website_index')
    else:
        form = PacientForm()
        form_user = UserRegisterForm

    return render(request, 'website/update.html', {'form': form, 'form_user':form_user})


def parse_disease(request):

    form_disease = GeneralForm(request.POST)
    date_pac = Pacient.objects.get(user=request.user)
    if str(date_pac.afectiune) == 'alzheimer':
        form_disease = AlzheimerForm(request.POST)
    elif str(date_pac.afectiune) == 'diabet':
        form_disease = AlzheimerForm(request.POST)
    elif str(date_pac.afectiune) == 'dementa':
        form_disease = AlzheimerForm(request.POST)
    elif str(date_pac.afectiune) == 'depresie':
        form_disease = AlzheimerForm(request.POST)

    return form_disease


def pacient_general_form_view(request):
    if request.method == 'POST':
        form = GeneralForm(request.POST)
        form_disease = parse_disease(request)

        if form.is_valid() and form_disease.is_valid():
            instance = form.save(commit=False)
            fd = form_disease.save(commit = False)

            instance.pacient = Pacient.objects.get(user = request.user)
            instance.rating = 100
            instance.save()
            return redirect('tutorial:website_index')
    else:
        form = GeneralForm()
        form_disease = parse_disease(request)
    return render(request, 'website/pacient_general_form.html', {'form': form, 'form_disease':form_disease})


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
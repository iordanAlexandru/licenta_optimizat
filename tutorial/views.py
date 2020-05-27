from django.core.mail import send_mail
from django.http import JsonResponse
from .models import Pacient, Tutore, PacientParsing, DepressionParsing, AlzheimerParsing, User
from django.contrib.auth.models import Group
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .decorators import restrict_unauthenticated_user, restrict_pacient_general_form, restrict_tutore_patient, tutore_and_admin_only, pacient_and_admin_only
from .forms import UserRegisterForm, PacientForm, GeneralForm, DepressionMoodForm, AlzheimerForm, DiabetesForm,DepressionForm, AlzheimerMoodForm
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
import numpy as np


class mood_results(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'website/mood_results.html')


def get_data(request, *args, **kwargs):

    data = {
        "user": 'alex',
        "nr_pacienti":111,
    }
    return JsonResponse(data)


class ChartDataAPI(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaa')
        print(self.request.user)
        users_no = User.objects.all().count()
        labels = ["users", "blue", "yellow", "green", "purple","orange"]
        default_items = [users_no, 34,21,32,15,22]
        data = {
            "labels":labels,
            "default":default_items,
        }
        return Response(data)


def index(request):
    context = {}
    if request.user.is_authenticated and request.user.groups.filter(name='pacient').exists():
        pacient = Pacient.objects.get(user=request.user)
        context = {'afectiune': pacient.afectiune, 'flag':pacient.flag}
    return render(request, 'website/index.html', context)


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
        form_disease = AlzheimerForm()
        if request.method == 'POST':
            form_disease = AlzheimerForm(request.POST)

    elif str(date_pac.afectiune) == 'diabet':
        form_disease = DiabetesForm()
        if request.method == 'POST':
            form_disease = DiabetesForm(request.POST)

    elif str(date_pac.afectiune) == 'depresie':
        form_disease = DepressionForm()
        if request.method == 'POST':
            form_disease = DepressionForm(request.POST)
    return form_disease


def calculate(param, type, question=None):
    rat=0
    if type=='tip1':
        if question == 'q1':
            if param=='1':
                rat += 30
            if param == '2':
                rat +=20
            if param == '3':
                rat +=10
        else:
            if param=='1':
                rat += 10
            if param == '2':
                rat += 5
            if param == '3':
                rat += 3
    if type == 'tip2':
        if param=='1':
            rat += 20
        if param == '2':
            rat +=10
        if param == '3':
            rat +=5
    return rat


def calculate_rating(request, fd, r1, r3): # e nevoie sa reverific boala pt rating
    r4 = fd.cleaned_data['c4']
    r5 = fd.cleaned_data['c5']
    r6 = fd.cleaned_data['c6']
    r = [r4,r5,r6]
    rating1 = [calculate(x,'tip2') for x in r]
    rating2_q1 = calculate(r1,'tip1', 'q1')
    rating2_q2 = calculate(r3,'tip1')
    rating = np.sum(rating1)+rating2_q1+rating2_q2
    return rating


@restrict_pacient_general_form
def pacient_general_form_view(request):
    if request.method == 'POST':
        form = GeneralForm(request.POST)
        form_disease = parse_disease(request)

        if form.is_valid() and form_disease.is_valid():
            instance = form.save(commit=False)
            fd = form_disease.save(commit = False)
            instance.pacient = Pacient.objects.get(user = request.user)
            r1 = form.cleaned_data['c1'] #general form parsing
            # r2 = form.cleaned_data['dorinta']  # tratata separat
            r3 = form.cleaned_data['c3']

            instance.rating = calculate_rating(request,form_disease,r1,r3)


            r2 = form.cleaned_data['dorinta']

            instance.activitate = r1
            instance.dorinta = r2
            instance.tip_fire = r3

            intr1 = form_disease.cleaned_data['c4']
            intr2 = form_disease.cleaned_data['c5']
            intr3 = form_disease.cleaned_data['c6']
            pac_pars = PacientParsing.objects.create(pacient = instance.pacient,
                                                     rating = instance.rating,
                                                     activitate = instance.activitate,
                                                     dorinta = instance.dorinta,
                                                     tip_fire = instance.tip_fire,
                                                     intrebare1 = intr1,
                                                     intrebare2= intr2,
                                                     intrebare3= intr3,
                                                     )
            instanta_pacient = Pacient.objects.get(user=request.user)
            instanta_pacient.flag= True
            instanta_pacient.save()
            return redirect('tutorial:website_index')
    else:
        form = GeneralForm()
        form_disease = parse_disease(request)
    return render(request, 'website/pacient_general_form.html', {'form': form, 'form_disease':form_disease})


def calcul_mood_form(form, afectiune):
    rating = 0
    if afectiune == 'depresie':
        for key, value in form.cleaned_data.items():
            rating = rating + int(value)
    if afectiune == 'alzheimer':
        for key, value in form.cleaned_data.items():
            rating = rating + int(value)
    return rating



def parse_mood_form(request, afectiune):
    form = None
    if afectiune == 'alzheimer':
        form = AlzheimerMoodForm()
        if request.method == 'POST':
            form = AlzheimerMoodForm(request.POST)
    if afectiune == 'depresie':
        form = DepressionMoodForm()
        if request.method == 'POST':
            form = DepressionMoodForm(request.POST)
    return form



def Average(lst):
    return sum(lst) / len(lst)


def creation_factory(user, pac_pars, afectiune, rating):
    p = Pacient.objects.get(user = user)
    if afectiune == 'alzheimer':
        try:
            instanta = AlzheimerParsing.objects.get(pacientparse=pac_pars)
            old_rating = instanta.disease_rating
            instanta.disease_rating = old_rating + ',' + str(rating)
            total_ratings = instanta.disease_rating.split(',')
            lista = []
            for x in total_ratings:
                lista.append(int(x))
            media = Average(lista)
            if len(total_ratings) % 3 == 0:
                send_mail(
                    'Mesaj informare pacient: ' + str(p),
                    'Punctajele pacientului dvs sunt urmatoarele: ' + str(instanta.disease_rating) + '\nMedia pacientului este: ' + str(round(media))
                    + '\n\n' +'Interpretarea Rezultatelor:\n5-8 – Creierul pacientului este intr-o stare buna.'
                    ' Daca acesta se relaxeaza mai des si mentine o dieta sanatoasa,'
                    ' creierul sau poate functiona mai bine\n'
                    '9-12 – Creierul pacientului este in pericol. Verifica-i dieta urgent ! Acesta poate sa reduca '
                    'pierderile de memorie cu vitamine, mancaruri care imbunatatesc functiile creierului, yoga, sport si meditatie.\n'
                    '12-15 – Creierul pacientului functioneaza in gol. Ar trebui de urgenta sa vada un doctor. '
                    'Acesta poate sa reduca pierderile de memorie alegand o dieta bogata in vitamine, sa mediteze, sa faca sport si sa se relaxeze mai des.\n'
                                                                                                     ,
                    'virtual_assistant@gov.com',
                    ['bpiwbpiw1@gmail.com'],
                    fail_silently=False,
                )
            instanta.save()
        except AlzheimerParsing.DoesNotExist:
            AlzheimerParsing.objects.create(pacientparse=pac_pars, disease_rating=rating, tutore=p.tutore)
    elif afectiune == 'depresie':
        try:
            instanta = DepressionParsing.objects.get(pacientparse=pac_pars)
            old_rating = instanta.disease_rating
            instanta.disease_rating = old_rating + ',' + str(rating)
            total_ratings = instanta.disease_rating.split(',')
            if len(total_ratings) % 3 == 0:
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                send_mail(
                    'Mesaj informare pacient: ' + str(p),
                    'Punctajele pacientului dvs sunt urmatoarele: ' + str(instanta.disease_rating) + '\nScor <= 15: Situatie grava\n'
                                                                                                 'Scor: [16-25]: Situatie ingrijoratoare\n'
                                                                                                 'Scor: [25-30]: Situatie acceptabila\n'
                                                                                                 'Scor >30: Situatie foarte buna ',
                    'virtual_assistant@gov.com',
                    ['bpiwbpiw1@gmail.com'],
                    fail_silently=False,
                )
            instanta.save()
        except DepressionParsing.DoesNotExist:
            DepressionParsing.objects.create(pacientparse=pac_pars, disease_rating=rating, tutore = p.tutore)



@pacient_and_admin_only
def MoodFormView(request):
    if request.method == 'POST':
        pacient = Pacient.objects.get(user=request.user)
        form = parse_mood_form(request, pacient.afectiune)
        if form.is_valid():
            rating = calcul_mood_form(form, pacient.afectiune)
            pacient_parsing = PacientParsing.objects.get(pacient = pacient)
            creation_factory(request.user, pacient_parsing,pacient.afectiune,rating)

    else:
        pacient = Pacient.objects.get(user=request.user)
        form = parse_mood_form(request, pacient.afectiune)
    context = {
        'form': form,
        'afectiune': pacient.afectiune
    }
    return render(request, 'website/mood_form.html', context)

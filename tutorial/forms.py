from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import Pacient, Tutore, PacientParsing
from django.core.validators import RegexValidator



class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']

class TutoreForm(forms.ModelForm):
    class Meta:
        model = Tutore
        fields = ['nr_pacienti']


selectie_boli= [
    ('alzheimer', 'Alzheimer'),
    ('diabet', 'Diabet'),
    ('depresie', 'Depresie'),
    ('singuratate', 'Singuratate'),
    ('dementa', 'Dementa'),
    ]


class PacientForm(forms.ModelForm):
    nume = forms.CharField(label='Nume:')
    prenume = forms.CharField(label='Prenume:')
    varsta = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    afectiune = forms.CharField(label='Afectiune:', widget=forms.Select(choices=selectie_boli))
    vaduv = forms.BooleanField(label='Vaduv:', required = False)
    parola_pacient = forms.CharField(label='Parola cont pacient:', widget=forms.PasswordInput)
    tel_urgenta = forms.CharField(max_length=10, validators=[RegexValidator(r'^\d{0,10}$')])


    class Meta:
        model = Pacient
        fields = [
            'nume',
            'prenume',
            'varsta',
            'afectiune',
            'vaduv',
            'parola_pacient',
            'tel_urgenta',
        ]

alegere_stil_viata= [
    ('sedentar', 'Nu fac sport si mananc des alimente nesanatoase'),
    ('normal', 'Mici scapari la dulciuri / fastfood'),
    ('activ','Fac sport si mananc sanatos regulat'),
    ]
alegere_fire=[
    ('extrovertit', 'Sunt extrovertit'),
    ('introvertit', 'Sunt introvertit'),
    ('depresiv', 'Am o stare depresiva uneori'),
]
alegere_dorinta= [
    ('conectare', 'Mi-ar placea sa fiu mai conectat cu tehnologia'),
    ('sanatate', 'As vrea sa imi pot schimba stilul de viata'),
    ('socializare','Vreau sa socializez mai mult'),
    ('normal','Nu vreau sa schimb nimic la mine'),
    ]


class GeneralForm(forms.ModelForm):
    activitate = forms.CharField(label='Care este stilul tau de viata?',
                                     widget=forms.Select(choices=alegere_stil_viata))
    dorinta = forms.CharField(label='Ce-ti doresti cel mai mult acum?',
                                     widget=forms.Select(choices=alegere_dorinta))
    tip_fire = forms.CharField(label='Ce fel de fire esti?',
                                     widget=forms.Select(choices=alegere_fire))
    rating = forms.IntegerField(widget = forms.HiddenInput(), required = False)
    class Meta:
        model = PacientParsing
        fields = [
            'activitate',
            'dorinta',
            'tip_fire',
            'rating',
        ]


class DiabetesForm(forms.ModelForm):
    dulciuri = forms.BooleanField(label='Obisnuiau sa iti placa dulciurile?',
                                     widget=forms.Select(choices=alegere_stil_viata))
    sport = forms.BooleanField(label='faci sport?',
                                     widget=forms.Select(choices=alegere_dorinta))
    dieta = forms.BooleanField(label='Ai o dieta echilibrata?',
                                     widget=forms.Select(choices=alegere_fire))
    nr_vizite_doctor = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    class Meta:
        model = Pacient
        fields = [
            'dulciuri',
            'sport',
            'nr_vizite_doctor'
        ]


class AlzheimerForm(forms.ModelForm):
    dulciuri = forms.BooleanField(label='Esti o fire organizata?',
                                     widget=forms.Select(choices=alegere_stil_viata))
    sport = forms.BooleanField(label='De obicei dormi des?',
                                     widget=forms.Select(choices=alegere_dorinta))
    dieta = forms.BooleanField(label='Atentia iti e distrasa usor?',
                                     widget=forms.Select(choices=alegere_fire))



class DementiaForm(forms.ModelForm):
    dulciuri = forms.BooleanField(label='Esti apreciat din cei din jur?',
                                     widget=forms.Select(choices=alegere_stil_viata))
    sport = forms.BooleanField(label='Esti o fire altruista?',
                                     widget=forms.Select(choices=alegere_dorinta))
    dieta = forms.BooleanField(label='Ai deseori o stare confuza?',
                                     widget=forms.Select(choices=alegere_fire))


class DepressionForm(forms.ModelForm):
    dulciuri = forms.BooleanField(label='Esti o fire organizata?',
                                     widget=forms.Select(choices=alegere_stil_viata))
    sport = forms.BooleanField(label='Iti place sa vizionezi filme?',
                                     widget=forms.Select(choices=alegere_dorinta))
    dieta = forms.BooleanField(label='Ti-ar placea sa te implici in diverse activitati?',
                                     widget=forms.Select(choices=alegere_fire))


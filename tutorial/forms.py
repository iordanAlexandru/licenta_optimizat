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
    ]


class PacientForm(forms.ModelForm):
    varsta = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    afectiune = forms.CharField(label='Afectiune:', widget=forms.Select(choices=selectie_boli))
    vaduv = forms.BooleanField(label='Vaduv:', required = False)
    tel_urgenta = forms.CharField(max_length=10, validators=[RegexValidator(r'^\d{0,10}$')])


    class Meta:
        model = Pacient
        fields = [
            'varsta',
            'afectiune',
            'vaduv',
            'tel_urgenta',
        ]

alegere_stil_viata= [
    ('3', 'Nu fac sport si mananc des alimente nesanatoase'),
    ('2', 'Mici scapari la dulciuri / fastfood'),
    ('1','Fac sport si mananc sanatos regulat'),
    ]
alegere_fire=[
    ('1', 'Sunt extrovertit'),
    ('2', 'Sunt introvertit'),
    ('3', 'Am o stare depresiva uneori'),
]

alegere_dorinta= [
    ('conectare', 'Mi-ar placea sa fiu mai conectat cu tehnologia'),
    ('sanatate', 'As vrea sa imi pot schimba stilul de viata'),
    ('socializare','Vreau sa socializez mai mult'),
    ('normal','Nu vreau sa schimb nimic la mine'),
    ]


class GeneralForm(forms.ModelForm):

    c1 = forms.ChoiceField(label='Care este stilul tau de viata?',choices=alegere_stil_viata,
                                     widget=forms.RadioSelect)
    dorinta = forms.ChoiceField(label='Ce-ti doresti cel mai mult acum?',choices=alegere_dorinta,
                                     widget=forms.RadioSelect)
    c3= forms.ChoiceField(label='Ce tip de fire esti?',choices=alegere_fire,
                                     widget=forms.RadioSelect)
    rating = forms.IntegerField(widget = forms.HiddenInput(), required = False)
    class Meta:
        model = PacientParsing
        fields = [
            'c1',
            'dorinta',
            'c3',
            'rating',
        ]


alegere_greutate= [
    ('1', 'Nu'),
    ('2', 'Nu stiu'),
    ('3','Da'),
    ]
alegere_stres= [
    ('1', 'Nu'),
    ('2', 'Nu stiu'),
    ('3','Da'),
    ]
alegere_dieta= [
    ('1', 'Da'),
    ('2', 'Cateodata mai mananc si ce nu trebuie'),
    ('3','Nu'),
    ]

class DiabetesForm(forms.ModelForm):
    c4 = forms.ChoiceField(label='Esti supraponderal/a?', choices=alegere_greutate,
                           widget=forms.RadioSelect)
    c5 = forms.ChoiceField(label='Esti o persoana care se streseaza usor?', choices=alegere_stres,
                           widget=forms.RadioSelect)
    c6 = forms.ChoiceField(label='Ai o dieta bine pusa la punct?', choices=alegere_dieta,
                           widget=forms.RadioSelect)
    class Meta:
        model = Pacient
        fields = [
            'c4',
            'c5',
            'c6'
        ]

alegere_stresAlz= [
    ('1', 'Nu'),
    ('2', 'Uneori'),
    ('3','Da'),
    ]
alegere_confuzie= [
    ('1', 'Nu'),
    ('2', 'Uneori'),
    ('3','Da'),
    ]
alegere_concentrare= [
    ('1', 'Da'),
    ('2', 'Uneori'),
    ('3','Nu'),
    ]

class AlzheimerForm(forms.ModelForm):
    c4= forms.ChoiceField(label='Te lasi stresat usor?',choices=alegere_stresAlz,
                                     widget=forms.RadioSelect)
    c5= forms.ChoiceField(label='Ai cateodata stari de confuzie?',choices=alegere_confuzie,
                                     widget=forms.RadioSelect)
    c6 = forms.ChoiceField(label='Reusesti cu greu sa te concentrezi?',choices=alegere_concentrare,
                                     widget=forms.RadioSelect)
    class Meta:
        model = Pacient
        fields = [
            'c4',
            'c5',
            'c6'
        ]


alegere_somn= [
    ('1', 'Nu'),
    ('2', 'Uneori'),
    ('3','Da'),
    ]
alegere_izolare= [
    ('1', 'Nu'),
    ('2', 'Cateodata'),
    ('3','Da'),
    ]
alegere_dietaDepr= [
    ('1', 'Da'),
    ('2', 'Uneori'),
    ('3','Nu'),
    ]


class DepressionForm(forms.ModelForm):
    c4 = forms.ChoiceField(label='Ai probleme cu somnul?', choices=alegere_somn,
                           widget=forms.RadioSelect)
    c5 = forms.ChoiceField(label='Ai momente cand te simti izolat?', choices=alegere_izolare,
                           widget=forms.RadioSelect)
    c6 = forms.ChoiceField(label='Ai o dieta echilibrata?', choices=alegere_dietaDepr,
                           widget=forms.RadioSelect)
    class Meta:
        model = Pacient
        fields = [
            # 'stare',
            'c4',
            'c5',
            'c6'
        ]
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import Pacient, Tutore, PacientParsing
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe


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
    ('2', 'Uneori'),
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

alegere_depr_mood= [
    ('1', 'Deloc'),
    ('2', 'Cateva zile'),
    ('3','Mai mult decat jumatate din zile'),
    ('4','Aproape in fiecare zi'),
    ]

class DepressionMoodForm(forms.ModelForm):
    c1 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani, cat de des ai fost deranjat de faptul ca '
                                 '<strong>n-ai avut stare, incat simteai nevoia de a te misca mai des decat de '
                                 'obicei?</strong>'), choices=alegere_depr_mood,
                           widget=forms.RadioSelect)
    c2 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani, cat de des ai fost deranjat de faptul ca '
                                           '<strong>vorbeai sau te miscai foarte incet incat alti oameni au '
                                           'observat acest lucru?</strong>'), choices=alegere_depr_mood,
                           widget=forms.RadioSelect)
    c3 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani, cat de des ai fost deranjat de faptul ca '
                                           '<strong>aveai probleme concentrandu-te asupra lucrurilor minore precum '
                                           'cititul sau vizionatul unor emisiuni</strong>'), choices=alegere_depr_mood,
                           widget=forms.RadioSelect)
    c4 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani, cat de des ai fost deranjat de faptul ca '
                                           '<strong>aveai o stima scazuta de sine - ca si cum ai fi un esec sau '
                                           'te-ai dezamagit pe tine sau familia?</strong>'), choices=alegere_depr_mood,
                           widget=forms.RadioSelect)
    c5 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani, cat de des ai fost deranjat de faptul ca '
                                           '<strong>n-ai mancat deloc sau ai mancat prea mult?</strong>'), choices=alegere_depr_mood,
                           widget=forms.RadioSelect)
    c6 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani, cat de des ai fost deranjat de faptul ca '
                                           '<strong>te simteai obosit sau nu aveai energie?</strong>'), choices=alegere_depr_mood,
                           widget=forms.RadioSelect)
    c7 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani, cat de des ai fost deranjat de faptul ca '
                                           '<strong>ai probleme cu somnul, adormi greu, dormi prea mult sau dormi'
                                           ' prea putin?</strong>'), choices=alegere_depr_mood,
                           widget=forms.RadioSelect)
    c8 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani, cat de des ai fost deranjat de faptul ca '
                                           '<strong>aveai o stare depresiva, te simteai prost sau fara speranta?'
                                           '</strong>'), choices=alegere_depr_mood,
                           widget=forms.RadioSelect)
    c9 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani, cat de des ai fost deranjat de faptul ca '
                                           '<strong> nu aveai interes sau placere in a face anumite lucruri'
                                           '</strong>'), choices=alegere_depr_mood,
                           widget=forms.RadioSelect)
    class Meta:
        model = PacientParsing
        fields = [
            'c1',
            'c2',
            'c3',
            'c4',
            'c5',
            'c6',
            'c7',
            'c8',
            'c9',
        ]

alegere_alzheimer_mood = [
    ('1','Da'),
    ('0','Nu'),
]
class AlzheimerMoodForm(forms.ModelForm):
    c1 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani ti s-a intamplat sa <strong>uiti in ce zi din saptamana'
                                           ' esti?</strong>'), choices=alegere_alzheimer_mood,
                           widget=forms.RadioSelect)
    c2 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani<strong>ai cautat vreun lucru si ai uitat ce anume cauti?</strong>'),
                           choices=alegere_alzheimer_mood,
                           widget=forms.RadioSelect)
    c3 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani ti s-a intamplat sa <strong>uiti vreun nume de-al prietenilor'
                                           ' tai? </strong>'),
                           choices=alegere_alzheimer_mood,
                           widget=forms.RadioSelect)
    c4 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani ti s-a intamplat sa <strong>aduni numere cu doua cifre '
                                           'si sa iti fie greu sa le calculezi din minte?</strong>'),
                           choices=alegere_alzheimer_mood,
                           widget=forms.RadioSelect)
    c5 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani ti s-a intamplat ca <strong>rareori sa te simti energic?</strong>'),
                           choices=alegere_alzheimer_mood,
                           widget=forms.RadioSelect)
    c6 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani <strong>te-au suparat mai des problemele minore decat de'
                                           ' obicei?</strong> '),
                           choices=alegere_alzheimer_mood,
                           widget=forms.RadioSelect)
    c7 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani ti s-a intamplat sa iti fie <strong>greu sa te concentrezi '
                                           'pentru macar o ora?</strong> '),
                           choices=alegere_alzheimer_mood,
                           widget=forms.RadioSelect)
    c8 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani ti s-a intamplat sa <strong>gasesti cheile undeva si nu-ti'
                                           ' amintesti faptul ca le-ai pus acolo?</strong>'),
                           choices=alegere_alzheimer_mood,
                           widget=forms.RadioSelect)
    c9 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani ti s-a intamplat sa <strong>te repeti de mai multe ori?</strong>'),
                           choices=alegere_alzheimer_mood,
                           widget=forms.RadioSelect)
    c10 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani ti s-a intamplat sa <strong>te pierzi undeva unde ai mai'
                                            ' fost inainte?</strong>'),
                           choices=alegere_alzheimer_mood,
                           widget=forms.RadioSelect)
    c11 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani ti s-a intamplat ca <strong>prietenii sau familia sa observe'
                                            ' ca esti mai uituc decat de obicei?</strong>'),
                           choices=alegere_alzheimer_mood,
                           widget=forms.RadioSelect)
    c12 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani ti s-a intamplat sa <strong>ratezi anumite intalniri /'
                                            ' programari din cauza ca ai uitat?</strong> '),
                           choices=alegere_alzheimer_mood,
                           widget=forms.RadioSelect)
    c13 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani ti s-a intamplat sa<strong> uiti punctul de vedere '
                                            'pe care voiai sa il spui?</strong>'),
                           choices=alegere_alzheimer_mood,
                           widget=forms.RadioSelect)
    c14 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani ti s-a intamplat sa<strong> depinzi de cafeina / bauturi '
                                            'energizante pentru a te putea concentra?</strong> '),
                           choices=alegere_alzheimer_mood,
                           widget=forms.RadioSelect)
    c15 = forms.ChoiceField(label=mark_safe('In ultimele doua saptamani ti s-a intamplat sa <strong>trebuiasca mai mult timp sa '
                                            'inveti lucruri care in mod normal ti-ar lua putin timp?</strong> '),
                           choices=alegere_alzheimer_mood,
                           widget=forms.RadioSelect)

    class Meta:
        model = PacientParsing
        fields = [
            'c1',
            'c2',
            'c3',
            'c4',
            'c5',
            'c6',
            'c7',
            'c8',
            'c9',
            'c10',
            'c11',
            'c12',
            'c13',
            'c14',
            'c15',
        ]


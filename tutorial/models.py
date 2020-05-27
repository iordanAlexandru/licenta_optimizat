from django.db import models
from django.contrib.auth.models import User
import json
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import int_list_validator


class Tutore(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='tutore'
    )

    nr_pacienti = models.IntegerField(default=0)
    flag = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Pacient(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='pacient'
    )

    varsta = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    afectiune = models.CharField(max_length=20)
    vaduv = models.BooleanField(default = False)
    tutore = models.ForeignKey(Tutore, on_delete=models.CASCADE)
    tel_urgenta = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{0,10}$')])
    flag = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

class PacientParsing(models.Model):
    pacient = models.ForeignKey(Pacient, on_delete=models.CASCADE)
    rating = models.IntegerField() #general_rating
    contor_forms = models.IntegerField(default=0)
    activitate = models.CharField(max_length=50)
    dorinta= models.CharField(max_length=50)
    tip_fire= models.CharField(max_length=50)
    intrebare1 = models.CharField(max_length=200, blank=True)
    intrebare2 = models.CharField(max_length=200, blank=True)
    intrebare3 = models.CharField(max_length=200, blank=True)
    contor_mesaje = models.IntegerField(default=0)
    _negative_problems = models.TextField(default='[]', blank=True)
    @property
    def problems(self):
        return json.loads(self._negative_problems)
    @problems.setter
    def problems(self,value):
        self._negative_problems = json.dumps(self.problems)

    def __str__(self):
        return str(self.pacient)


class PacientDetails(models.Model):
    pacient = models.ForeignKey(Pacient,on_delete=models.CASCADE)
    fav_book = models.CharField( max_length=200, default='')
    fav_movie = models.CharField(max_length=200, default='')
    fav_song = models.CharField(max_length = 200, default='')
    fav_activity= models.CharField(max_length=200, default='')
    fav_passion = models.CharField(max_length= 200, default='')
    fav_game = models.CharField(max_length = 200, default='')
    hangout = models.IntegerField( default = 0)

    def __str__(self):
        return str(self.pacient)


class DepressionParsing(models.Model):
    pacientparse = models.ForeignKey(PacientParsing, on_delete=models.CASCADE)
    disease_rating = models.CharField(default=0, validators=[int_list_validator], max_length=100)
    tutore = models.ForeignKey(Tutore, on_delete=models.CASCADE,  null=True)
    def __str__(self):
        return str(self.pacientparse)


class AlzheimerParsing(models.Model):
    pacientparse = models.ForeignKey(PacientParsing, on_delete=models.CASCADE)
    disease_rating = models.CharField(default=0, validators=[int_list_validator], max_length=100)
    tutore = models.ForeignKey(Tutore, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.pacientparse)


class DiabetesParsing(models.Model):
    pacientparse = models.ForeignKey(PacientParsing, on_delete=models.CASCADE)
    disease_rating = models.CharField(default=0, validators=[int_list_validator], max_length=100)
    tutore = models.ForeignKey(Tutore, on_delete=models.CASCADE,  null=True)
    def __str__(self):
        return str(self.pacientparse)


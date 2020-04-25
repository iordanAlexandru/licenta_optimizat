from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator

class Pacient(models.Model):
    nume = models.CharField(max_length=20)
    prenume = models.CharField(max_length=20)
    varsta = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    afectiune = models.CharField(max_length=20)
    vaduv = models.BooleanField(default = False)
    parola_pacient = models.CharField(max_length=20)
    tutore = models.CharField(default='', max_length=20)
    user_pacient = models.CharField(default ='', max_length=20)
    tel_urgenta = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{0,10}$')])

    def __str__(self):
        return self.prenume

class PacientParsing(models.Model):
    pacient = models.ForeignKey(Pacient, on_delete=models.CASCADE)
    rating = models.IntegerField()
    activitate = models.CharField(max_length=50)
    dorinta= models.CharField(max_length=50)
    tip_fire= models.CharField(max_length=50)

    def __str__(self):
        return self.rating

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

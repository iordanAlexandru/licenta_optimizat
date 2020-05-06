from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator

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

    def __str__(self):
        return self.user.username

class PacientParsing(models.Model):
    pacient = models.ForeignKey(Pacient, on_delete=models.CASCADE)
    rating = models.IntegerField() #general_rating
    activitate = models.CharField(max_length=50)
    dorinta= models.CharField(max_length=50)
    tip_fire= models.CharField(max_length=50)
    # cele 3 campuri specifice bolii
    #flag
    #mood_rating
    def __str__(self):
        return str(self.pacient)

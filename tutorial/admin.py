from django.contrib import admin
from .models import Pacient, Tutore, PacientParsing, DepressionParsing,AlzheimerParsing,DiabetesParsing

admin.site.register(Pacient)
admin.site.register(PacientParsing)
admin.site.register(Tutore)
admin.site.register(DepressionParsing)
admin.site.register(AlzheimerParsing)
admin.site.register(DiabetesParsing)
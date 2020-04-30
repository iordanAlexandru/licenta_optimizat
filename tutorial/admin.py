from django.contrib import admin
from .models import Pacient, Tutore, PacientParsing

admin.site.register(Pacient)
admin.site.register(PacientParsing)
admin.site.register(Tutore)
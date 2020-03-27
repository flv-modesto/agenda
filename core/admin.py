from django.contrib import admin
from core.models import Evento
# Register your models here.

class EventAdmin (admin.ModelAdmin):
    list_display = ('titulo', 'data_evento','data_criacao')

admin.site.register(Evento, EventAdmin)
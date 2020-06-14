from django.contrib import admin
from core.models import Evento
# Register your models here.

class EventAdmin (admin.ModelAdmin):
    list_display = ('id', 'titulo', 'data_evento','data_criacao','descricao', 'localidade')
    list_filter = ('usuario', 'data_evento',)
admin.site.register(Evento, EventAdmin)
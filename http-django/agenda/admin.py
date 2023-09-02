from django.contrib import admin

from agenda.models import Categoria, Evento


admin.site.register(Categoria)
admin.site.register(Evento)
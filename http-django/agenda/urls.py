from django.urls import path

from agenda.views import categoria_list, evento_list, evento_detail, evento_actions


urlpatterns = [
  path("categorias/", categoria_list, name="categoria_list"),
  path("eventos/", evento_list, name="evento_list"),
  path("eventos/<int:id>/", evento_detail, name="evento_detail"),
  path("eventos/actions", evento_actions, name="evento_actions"),
]
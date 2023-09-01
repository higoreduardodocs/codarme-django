from django.urls import path

from agenda.views import horarios_list, AgendamentoList, AgendamentoDetail, PrestadorList


urlpatterns = [
  path("agendamentos/horarios/", horarios_list),
  path("agendamentos/", AgendamentoList.as_view()),
  path("agendamentos/<int:id>/", AgendamentoDetail.as_view()),
  path("agendamentos/prestadores/", PrestadorList.as_view()),
]
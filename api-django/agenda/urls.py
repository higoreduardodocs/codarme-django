from django.urls import path

from agenda.views import horarios_list, AgendamentoList, AgendamentoDetail


urlpatterns = [
  path("agendamentos/horarios/", horarios_list),
  path("agendamentos/", AgendamentoList.as_view()),
  path("agendamentos/<int:id>/", AgendamentoDetail.as_view()),
]
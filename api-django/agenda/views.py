from rest_framework import generics
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from datetime import datetime

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer
from agenda.utils import get_horarios_disponiveis

@api_view(http_method_names=["GET"])
def horarios_list(request):
  data_agendamento = request.query_params.get("data_agendamento")
  if not data_agendamento:
    data_agendamento = datetime.now().date()
  else:
    data_agendamento = datetime.fromisoformat(data_agendamento).date()
  
  horarios_disponiveis = sorted(list(get_horarios_disponiveis(data_agendamento)))
  return JsonResponse(horarios_disponiveis, safe=False)

class AgendamentoList(generics.ListCreateAPIView):
  queryset = Agendamento.objects.all()
  serializer_class = AgendamentoSerializer

class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Agendamento.objects.all()
  serializer_class = AgendamentoSerializer
  lookup_field = "id"
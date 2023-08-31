from rest_framework import generics

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer

class AgendamentoList(generics.ListCreateAPIView):
  queryset = Agendamento.objects.all()
  serializer_class = AgendamentoSerializer


class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Agendamento.objects.all()
  serializer_class = AgendamentoSerializer
  lookup_field = "id"
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from datetime import datetime

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer, PrestadorSerializer
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

class IsOnwerOrCreateOnly(permissions.BasePermission):
  def has_permission(self, request, view):
    if request.method == "POST":
      return True
    
    username = request.query_params.get("username", "")
    if request.user.username == username:
      return True
    return False

class AgendamentoList(generics.ListCreateAPIView):
  serializer_class = AgendamentoSerializer
  permission_classes = [IsOnwerOrCreateOnly]

  def get_queryset(self):
    username = self.request.query_params.get("username", None)
    queryset = Agendamento.objects.filter(prestador__username=username)
    return queryset
  
class IsPrestador(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if obj.prestador == request.user:
      return True
    return False

class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Agendamento.objects.all()
  serializer_class = AgendamentoSerializer
  lookup_field = "id"
  permission_classes = [IsPrestador]

  def perform_destroy(self, instance):
    instance.cancelado = True
    instance.save()

class PrestadorList(generics.ListAPIView):
  queryset = User.objects.all()
  serializer_class = PrestadorSerializer
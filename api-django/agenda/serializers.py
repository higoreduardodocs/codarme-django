from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone

from agenda.models import Agendamento
from agenda.utils import get_horarios_disponiveis


class AgendamentoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Agendamento
    fields = '__all__'

  prestador = serializers.CharField()

  def validate_prestador(self, value):
    try:
      prestador_obj = User.objects.get(username=value)
    except User.DoesNotExist:
      raise serializers.ValidationError("Prestador não encontrado")
    
    return prestador_obj
  
  def validate_data_agendamento(self, value):
    if value < timezone.now():
      raise serializers.ValidationError("Horário de agendamento expirado")
    if value not in get_horarios_disponiveis(value.date()):
      raise serializers.ValidationError("Horário indisponível")
    
    return value
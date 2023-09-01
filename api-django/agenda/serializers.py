from rest_framework import serializers

from agenda.models import Agendamento
from django.contrib.auth.models import User


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
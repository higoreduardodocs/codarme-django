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
  
  def validate(self, attrs):
    email_cliente = attrs.get("email_cliente", "")
    telefone_cliente = attrs.get("telefone_cliente", "")
    data_agendamento = attrs.get("data_agendamento", "")

    if email_cliente.endswith(".br") and telefone_cliente.startswith("+") and not telefone_cliente.startswith("+55"):
      raise serializers.ValidationError("Contatos do cliente devem ser do mesmo país de origem")
    if Agendamento.objects.filter(email_cliente=email_cliente, data_agendamento=data_agendamento).exists():
      raise serializers.ValidationError("Cliente já reservou o horário")
    
    return attrs
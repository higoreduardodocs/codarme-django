from rest_framework import serializers

from agenda.models import Agendamento

class AgendamentoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Agendamento
    fields = '__all__'
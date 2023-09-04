from rest_framework import serializers
from datetime import date
from django.contrib.auth.models import User

from agenda.models import Agendamento, AgendamentoCustom

class AgendamentoSerializer(serializers.Serializer):
  data_agendamento = serializers.DateTimeField()
  nome_cliente = serializers.CharField(max_length=200)
  email_cliente = serializers.EmailField()
  telefone_cliente = serializers.CharField(max_length=20)

class AgendamentoSerializerCreateUpdate(serializers.Serializer):
  data_agendamento = serializers.DateTimeField()
  nome_cliente = serializers.CharField(max_length=200)
  email_cliente = serializers.EmailField()
  telefone_cliente = serializers.CharField(max_length=20)

  def validate_data_agendamento(self, value):
    """Validação customizada do campo 'data_agendamento'"""
    if value.date() < date.today():
      raise serializers.ValidationError("Horário expirado")
    return value
  
  def validate(self, attrs):
    """Validação de nível de objeto (validate object-level)"""
    email_cliente = attrs.get("email_cliente", "")
    telefone_cliente = attrs.get("telefone_cliente", "")

    if email_cliente.endswith(".br") and telefone_cliente.startswith("+") and not telefone_cliente.startswith("+55"):
      raise serializers.ValidationError("Contatos de países diferentes são inválidos")
    return attrs

  def create(self, validated_data):
    agendamento = Agendamento.instanceects.create(
      data_agendamento=validated_data["data_agendamento"],
      nome_cliente=validated_data["nome_cliente"],
      email_cliente=validated_data["email_cliente"],
      telefone_cliente=validated_data["telefone_cliente"]
    )
    return agendamento
  
  def update(self, instance, validated_data):
    instance.data_agendamento = validated_data.get("data_agendamento", instance.data_agendamento)
    instance.nome_cliente = validated_data.get("nome_cliente", instance.nome_cliente)
    instance.email_cliente = validated_data.get("email_cliente", instance.email_cliente)
    instance.telefone_cliente = validated_data.get("telefone_cliente", instance.telefone_cliente)
    instance.save()
    return instance
  
class AgendamentoSerializerModelSerialiazer(serializers.ModelSerializer):
  class Meta:
    model = Agendamento
    fields = ['id', 'data_agendamento', 'nome_cliente', 'email_cliente', 'telefone_cliente']

  def validate_data_agendamento(self, value):
    if value.date() < date.today():
      raise serializers.ValidationError("Horário expirado")
    return value
  
  def validate(self, attrs):
    email_cliente = attrs.get("email_cliente", "")
    telefone_cliente = attrs.get("telefone_cliente", "")

    if email_cliente.endswith(".br") and telefone_cliente.startswith("+") and not telefone_cliente.startswith("+55"):
      raise serializers.ValidationError("Contatos de países diferentes são inválidos")
    return attrs
  
class AgendamentoSerializerModelSerialiazerCustom(serializers.ModelSerializer):
  class Meta:
    model = AgendamentoCustom
    fields = '__all__'
  
  # Validação de tipos (int, str)
  # Validação específica (validate_prestador)
  # Validaçao objeto (validate)
  prestador = serializers.CharField()

  def validate_prestador(self, value):
    try:
      obj = User.objects.get(username=value)
    except User.DoesNotExist:
      raise serializers.ValidationError("Usuário não existe")
    return obj
  
class PrestadorSerializerModelSerializerCustom(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'agendamentos']

    agendamentos = AgendamentoSerializerModelSerialiazerCustom(many=True, read_only=True)
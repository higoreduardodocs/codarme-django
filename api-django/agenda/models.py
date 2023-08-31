from django.db import models


class Agendamento(models.Model):
  data_agendamento = models.DateTimeField()
  nome_cliente = models.CharField(max_length=200)
  email_cliente = models.EmailField()
  telefone_cliente = models.CharField(max_length=20)
  cancelado = models.BooleanField(default=False)

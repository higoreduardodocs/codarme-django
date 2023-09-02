from django.db import models


class Categoria(models.Model):
  nome = models.CharField(max_length=255)

  def __str__(self):
    return f"{self.nome} <{self.id}>"


class Evento(models.Model):
  nome = models.CharField(max_length=255)
  categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
  local = models.CharField(max_length=255, blank=True)
  link = models.CharField(max_length=255, blank=True)
  data = models.DateField(null=True)
  participantes = models.IntegerField(default=0)

  def __str__(self):
    return f"{self.nome} <{self.id}>"

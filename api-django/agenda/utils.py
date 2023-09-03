from typing import Iterable
from datetime import date, datetime, timezone, timedelta

from agenda.models import Agendamento
from agenda.libs import brasil_api


def get_horarios_disponiveis(data: date) -> Iterable[datetime]:
  """
  Retorna uma lista com objetos do tipo datetime cujas datas são o mesmo dia passado (data)
  e os horários são os horários disponíveis para aquele dia, conforme outros agendamentos existam.
  Limpando datas de feriados do horário de almoço 11-13h
  """
  try:
    if brasil_api.is_feriado(data):
      return []
  except ValueError:
    ...

  start = datetime(year=data.year, month=data.month, day=data.day, hour=9, minute=0, second=0, tzinfo=timezone.utc)
  end = datetime(year=data.year, month=data.month, day=data.day, hour=17, minute=30, second=0, tzinfo=timezone.utc)
  delta = timedelta(minutes=30)

  horarios_disponiveis = []
  while start <= end:
    if not Agendamento.objects.filter(data_agendamento=start).exists() and not start.hour in (11, 12):
      horarios_disponiveis.append(start)
    start = start + delta

  return horarios_disponiveis
from datetime import date
from django.conf import settings
import requests
import logging


def is_feriado(data: date) -> bool:
  logging.info(f"Consumindo Brasil API: {data.isoformat()}")
  if settings.TESTING == True:
    logging.info("TESTING=True não fazendo requisições a Brasil API")
    if data.day == 25 and data.month == 12:
      return True
    return False

  ano = data.year
  r = requests.get(f"https://brasilapi.com.br/api/feriados/v1/{ano}")
  if r.status_code != 200:
    logging.error("Falha no consumo da Brasil API")
    raise ValueError("Algum problema ocorreu na Brasil API")
  
  feriados = r.json()
  for feriado in feriados:
    data_feriado = date.fromisoformat(feriado["date"])
    if data_feriado == data:
      return True
    
  return False
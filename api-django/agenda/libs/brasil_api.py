from datetime import date
import requests


def is_feriado(data: date) -> bool:
  ano = data.year
  r = requests.get(f"https://brasilapi.com.br/api/feriados/v1/{ano}")
  if r.status_code != 200:
    raise ValueError("Algum problema ocorreu na Brasil API")
  
  feriados = r.json()
  for feriado in feriados:
    data_feriado = date.fromisoformat(feriado["date"])
    if data_feriado == data:
      return True
    
  return False
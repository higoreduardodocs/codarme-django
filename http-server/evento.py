import json

class Evento:
  id = 1

  def __init__(self, nome, local=""):
    self.nome= nome
    self.local = local
    Evento.id += 1

  @classmethod
  def evento_online(cls, nome):
    evento = cls(nome, f"http://localhost:3000/eventos/?id={cls.id}")
    return evento
  
  @staticmethod
  def area_por_pessoa(area):
    if 5 <= area < 10:
      return 5
    elif 10 <= area < 20:
      return 10
    elif area > 20:
      return 20
    else:
      return 0

  def mostra_dados(self):
    print(f"ID: {self.id} | Nome: {self.nome} | Local: {self.local}")

  def to_json(self):
    # return self.__dict__
    return json.dumps({
      "id": self.id, "nome": self.nome, "local": self.local
    })
  
class EventoOnline(Evento):
  def __init__(self, nome, _=""):
    local = f"http://localhost:3000/eventos/id={EventoOnline.id}"
    super().__init__(nome, local)

  def mostra_dados(self):
    print(f"ID: {self.id} | Nome: {self.nome} | Link: {self.local}")
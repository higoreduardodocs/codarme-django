from datetime import timedelta, date


class Tarefa:
  def __init__(self, titulo, descricao="", data=None, notificacao=None):
    self.titulo = titulo
    self.descricao = descricao
    self.data = data
    self.notificaco = notificacao
    self.concluida = False

  def concluir(self):
    self.concluida = True

  def adicionar_descricao(self, descricao):
    self.descricao = descricao

  def adiar_notificacao(self, minutos):
    self.data += timedelta(minutes=minutos)

  def is_atrasada(self):
    return self.data.date() < date.today()
  
class TarefaList:
  def __init__(self):
    self._tarefas = []
    self._quantidade_tarefas = 0

  def adicionar_tarefa(self, tarefa):
    self._tarefas.append(tarefa)
    self._quantidade_tarefas += 1

  def quantidade_tarefas(self):
    return self._quantidade_tarefas

  def listar_tarefas(self, pendentes=True):
    tarefas = []
    if not pendentes:
      for tarefa in self._tarefas:
        if tarefa.concluida:
          tarefas.append(tarefa)

      return tarefas
    
    return self._tarefas
  
  def listar_atrasadas(self):
    tarefas = []
    for tarefa in self._tarefas:
      if tarefa.data and not tarefa.concluida and tarefa.data.date() < date.today():
        tarefas.append(tarefa)

    return tarefas
  
  def lista_do_dia(self):
    tarefas = []
    for tarefa in self._tarefas:
      if tarefa.data and not tarefa.concluida and tarefa.data.date() == date.today():
        tarefas.append(tarefa)

    return tarefas
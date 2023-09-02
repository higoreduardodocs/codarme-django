import unittest
from datetime import datetime, timezone

from tarefa import Tarefa, TarefaList


# TAREFA
class TestConcluir(unittest.TestCase):
  def test_concluir_tarefa_true(self):
    tarefa = Tarefa("Estudar python")
    tarefa.concluir()

    self.assertEqual(tarefa.concluida, True)

  def test_concluir_tarefa_mantem_true(self):
    tarefa = Tarefa("Estudar python")
    tarefa.concluir()

    self.assertEqual(tarefa.concluida, True)
    tarefa.concluir()

    self.assertEqual(tarefa.concluida, True)

class TestDescricao(unittest.TestCase):
  def test_adicionar_descricao(self):
    tarefa = Tarefa("Estudar python")
    tarefa.adicionar_descricao("Estudar testes automatizados")

    self.assertNotEqual(tarefa.descricao, "")
    self.assertEqual(tarefa.descricao, "Estudar testes automatizados")

  def test_editar_descricao(self):
    tarefa = Tarefa("Estudar python")
    tarefa.adicionar_descricao("Estudar testes automatizados")

    self.assertNotEqual(tarefa.descricao, "")
    self.assertEqual(tarefa.descricao, "Estudar testes automatizados")

    tarefa.adicionar_descricao("Estudar try-except")

    self.assertNotEqual(tarefa.descricao, "Estudar testes automatizados")
    self.assertEqual(tarefa.descricao, "Estudar try-except")

class TestAdiar(unittest.TestCase):
  def test_adiar_15_min(self):
    date_original = datetime(2023, 10, 20, 10, 30, tzinfo=timezone.utc)
    date_esperado = datetime(2023, 10, 20, 10, 45, tzinfo=timezone.utc)
    tarefa = Tarefa("Estudar python", data=date_original)
    tarefa.adiar_notificacao(15)
    if tarefa.data == None:
      return

    self.assertNotEqual(tarefa.data, date_original)
    self.assertEqual(tarefa.data, date_esperado)

class TestIsAtrasda(unittest.TestCase):
  def test_tarefa_atrasada(self):
    tarefa = Tarefa("Estudar python", data=datetime(2023, 5, 20, 10, 30, tzinfo=timezone.utc))

    self.assertEqual(tarefa.is_atrasada(), True)

  def test_tarefa_prazo(self):
    tarefa = Tarefa("Estudar python", data=datetime(2023, 10, 20, 10, 30, tzinfo=timezone.utc))

    self.assertNotEqual(tarefa.is_atrasada(), True)

# LISTA TAREFA
class TestTarefaList(unittest.TestCase):
  def test_adicionar_tarefa(self):
    python = Tarefa("Estudar python")
    typescript = Tarefa("Estudar typescript")

    lista = TarefaList()
    lista.adicionar_tarefa(python)
    lista.adicionar_tarefa(typescript)

    self.assertNotEqual(lista.quantidade_tarefas(), 0)
    self.assertEqual(lista.quantidade_tarefas(), 2)
    self.assertEqual(lista.listar_tarefas(), [python, typescript])

  def test_tarefas_concluidas(self):
    python = Tarefa("Estudar python")
    typescript = Tarefa("Estudar typescript")
    python.concluir()

    lista = TarefaList()
    lista.adicionar_tarefa(python)
    lista.adicionar_tarefa(typescript)

    self.assertEqual(lista.listar_tarefas(pendentes=False), [python])

  def test_tarefas_atrasadas(self):
    python = Tarefa("Estudar python", data=datetime(2023, 9, 1, 10, 30, tzinfo=timezone.utc))
    typescript = Tarefa("Estudar typescript", data=datetime(2023, 9, 2, 10, tzinfo=timezone.utc))

    lista = TarefaList()
    lista.adicionar_tarefa(python)
    lista.adicionar_tarefa(typescript)

    self.assertEqual(lista.listar_atrasadas(), [python])

  def test_tarefas_do_dia(self):
    python = Tarefa("Estudar python", data=datetime(2023, 9, 2, 10, 30, tzinfo=timezone.utc))
    typescript = Tarefa("Estudar typescript", data=datetime(2023, 9, 2, 10, tzinfo=timezone.utc))

    lista = TarefaList()
    lista.adicionar_tarefa(python)
    lista.adicionar_tarefa(typescript)

    self.assertEqual(lista.lista_do_dia(), [python, typescript])

unittest.main()
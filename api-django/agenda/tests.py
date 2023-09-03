from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from datetime import datetime, timezone
from unittest import mock
import json

from agenda.models import Agendamento


class obj:
  def __init__(self, dict):
    self.__dict__.update(dict)

def create_usuario():
  return User.objects.create(
      email="bhigoreduardo@email.com",
      username="bhigoreduardo",
      password="admin"
    )

def create_agendamento(prestador):
  Agendamento.objects.create(
    data_agendamento=datetime(2023, 9, 20, tzinfo=timezone.utc),
    nome_cliente="Cliente",
    email_cliente="email@email.com",
    telefone_cliente="123456789",
    prestador=prestador
  )
  return {
      "id": 1,
      "data_agendamento": "2023-09-20T00:00:00Z",
      "nome_cliente": "Cliente",
      "email_cliente": "email@email.com",
      "telefone_cliente": "123456789",
      "cancelado": False,
      "prestador": prestador.username
    }

def create_request(prestador, is_fora_expediente=False, is_feriado=False, is_almoco=False, is_passado=False, is_contato_extrangeiros=False):
  request = {
      "data_agendamento": "2023-09-20T10:00:00Z",
      "nome_cliente": "Cliente",
      "email_cliente": "email@email.com",
      "telefone_cliente": "123456789",
      "prestador": prestador.username
    }

  if is_fora_expediente:
    request["data_agendamento"] = "2023-09-20T07:00:00Z"
  elif is_feriado:
    request["data_agendamento"] = "2023-12-25T09:00:00Z"
  elif is_almoco:
    request["data_agendamento"] = "2023-09-20T11:30:00Z"
  elif is_passado:
    request["data_agendamento"] = "2023-07-20T09:30:00Z"
  elif is_contato_extrangeiros:
    request["email_cliente"] = "email@email.com.br"
    request["telefone_cliente"] = "+45678123"
  
  return request

class TestAgendamentoList(APITestCase):
  # Mock
  def test_cria_agendamento(self):
    user = create_usuario()
    request = create_request(user)

    response = self.client.post("/api/agendamentos/", request, format="json")
    agendamento = Agendamento.objects.get()

    self.assertEqual(response.status_code, 201)
    self.assertEqual(agendamento.data_agendamento, datetime(2023, 9, 20, 10, tzinfo=timezone.utc))

  # Mock
  def test_cria_agendamento_fora_expediente(self):
    user = create_usuario()
    request = create_request(user, is_fora_expediente=True)
    
    response = self.client.post("/api/agendamentos/", request, format="json")
    agendamentos = Agendamento.objects.all()
    
    self.assertEqual(response.status_code, 400)
    self.assertEqual(list(agendamentos), [])

  # Mock
  def test_cria_agendamento_feriado(self):
    user = create_usuario()
    request = create_request(user, is_feriado=True)

    response = self.client.post("/api/agendamentos/", request, format="json")
    agendamentos = Agendamento.objects.all()

    self.assertEqual(response.status_code, 400)
    self.assertEqual(list(agendamentos), [])

  # Mock
  def test_cria_agendamento_almoco(self):
    user = create_usuario()
    request = create_request(user, is_almoco=True)

    response = self.client.post("/api/agendamentos/", request, format="json")
    agendamentos = Agendamento.objects.all()

    self.assertEqual(response.status_code, 400)
    self.assertEqual(list(agendamentos), [])

  # Mock
  def test_cria_agendamento_prestador_404(self):
    user = json.loads(json.dumps({"username": "bhigoreduardo"}), object_hook=obj)
    request = create_request(user)

    response = self.client.post("/api/agendamentos/", request, format="json")
    agendamentos = Agendamento.objects.all()

    self.assertEqual(response.status_code, 400)
    self.assertEqual(list(agendamentos), [])

  # Mock
  def test_Cria_agendamento_data_passado(self):
    user = create_usuario()
    request = create_request(user, is_passado=True)

    response = self.client.post("/api/agendamentos/", request, format="json")
    agendamentos = Agendamento.objects.all()

    self.assertEqual(response.status_code, 400)
    self.assertEqual(list(agendamentos), [])

  # Mock
  def test_cria_agendamento_contatos_paises_diferentes(self):
    user = create_usuario()
    request = create_request(user, is_contato_extrangeiros=True)

    response = self.client.post("/api/agendamentos/", request, format="json")
    agendamentos = Agendamento.objects.all()

    self.assertEqual(response.status_code, 400)
    self.assertEqual(list(agendamentos), [])

  # Mock
  def test_cria_agendamento_repetido(self):
    user = create_usuario()
    request = create_request(user)

    response = self.client.post("/api/agendamentos/", request, format="json")
    agendamentos = Agendamento.objects.all()

    self.assertEqual(response.status_code, 201)
    self.assertEqual(len(list(agendamentos)), 1)

    response = self.client.post("/api/agendamentos/", request, format="json")
    agendamentos = Agendamento.objects.all()

    self.assertEqual(response.status_code, 400)
    self.assertEqual(len(list(agendamentos)), 1)

  def test_listagem_sem_auth(self):
    user = create_usuario()

    response = self.client.get("/api/agendamentos/?username=bhigoreduardo")
    self.assertEqual(response.status_code, 403)

  def test_listagem_com_auth_vazia(self):
    user = create_usuario()

    self.client.force_authenticate(user)
    # self.client.login(username="bhigoreduardo", password="admin")
    response = self.client.get("/api/agendamentos/?username=bhigoreduardo")

    data = json.loads(response.content)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data, [])

  def test_listagem_com_auth(self):
    user = create_usuario()
    agendamento_serializer = create_agendamento(user)

    self.client.force_authenticate(user)
    response = self.client.get("/api/agendamentos/?username=bhigoreduardo")

    data = json.loads(response.content)
    self.assertEqual(response.status_code, 200)
    self.assertNotEqual(data, [])
    self.assertEqual(data[0], agendamento_serializer)
    self.assertDictEqual(data[0], agendamento_serializer)

class TestAgendamentoDetail(APITestCase):
  def test_detalhe_sem_auth(self):
    user = create_usuario()
    create_agendamento(user)

    response = self.client.get("/api/agendamentos/1/?username=bhigoreduardo")

    self.assertEqual(response.status_code, 403)

  def test_detalhe_com_auth(self):
    user = create_usuario()
    agendamento_serializer = create_agendamento(user)

    self.client.force_authenticate(user)
    response = self.client.get("/api/agendamentos/1/?username=bhigoreduardo")

    self.assertEqual(response.status_code, 200)
    self.assertEqual(json.loads(response.content), agendamento_serializer)

  def test_detalhe_404(self):
    user = create_usuario()

    self.client.force_authenticate(user)
    response = self.client.get("/api/agendamentos/1/?username=bhigoreduardo")

    self.assertEqual(response.status_code, 404)

  def test_detalhe_prestador_404(self):
    response = self.client.get("/api/agendamentos/1/?username=bhigoreduardo")

    self.assertEqual(response.status_code, 404)

  def test_atualizacao_put(self):
    user = create_usuario()
    agendamento_serializer = create_agendamento(user)
    agendamento_serializer["data_agendamento"] = "2023-11-10T10:00:00Z"

    self.client.force_authenticate(user)
    response = self.client.put("/api/agendamentos/1/", agendamento_serializer)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(json.loads(response.content), agendamento_serializer)

  def test_atualizacao_patch(self):
    user = create_usuario()
    agendamento_serializer = create_agendamento(user)

    self.client.force_authenticate(user)
    response = self.client.patch("/api/agendamentos/1/", {"data_agendamento": "2023-09-15T15:00:00Z"})
    agendamento = Agendamento.objects.get()
    agendamento_serializer["data_agendamento"] = "2023-09-15T15:00:00Z"
    date_format = '%Y-%m-%dT%H:%M:%S%z'

    self.assertEqual(response.status_code, 200)
    self.assertEqual(json.loads(response.content), agendamento_serializer)
    self.assertEqual(agendamento.data_agendamento, datetime(2023, 9, 15, 15, tzinfo=timezone.utc))
    self.assertEqual(datetime.strptime(agendamento_serializer["data_agendamento"], date_format), datetime(2023, 9, 15, 15, tzinfo=timezone.utc))

  def test_atualizacao_sem_auth(self):
    user = create_usuario()
    agendamento_serializer = create_agendamento(user)

    response = self.client.patch("/api/agendamentos/1/", {"data_agendamento": "2023-09-15T15:00:00Z"})
    agendamento = Agendamento.objects.get()
    date_format = '%Y-%m-%dT%H:%M:%S%z'

    self.assertEqual(response.status_code, 403)
    self.assertEqual(agendamento.data_agendamento, datetime.strptime(agendamento_serializer["data_agendamento"], date_format))

  # Mock
  def test_atualizacao_data_agendamento(self):
    user = create_usuario()
    create_agendamento(user)

    self.client.force_authenticate(user)
    response = self.client.patch("/api/agendamentos/1/", {"data_agendamento": "2023-09-15T15:00:00Z"})
    agendamento = Agendamento.objects.get()
    date_format = '%Y-%m-%dT%H:%M:%S%z'

    self.assertEqual(response.status_code, 200)
    self.assertEqual(agendamento.data_agendamento,
                     datetime.strptime(json.loads(response.content)["data_agendamento"], date_format))

  def test_cancelamento(self):
    user = create_usuario()
    create_agendamento(user)

    self.client.force_authenticate(user)
    response = self.client.delete("/api/agendamentos/1/")
    agendamento = Agendamento.objects.get()

    self.assertEqual(response.status_code, 204)
    self.assertEqual(agendamento.cancelado, True)

    response = self.client.delete("/api/agendamentos/1/")
    agendamento = Agendamento.objects.get()

    self.assertEqual(response.status_code, 204)
    self.assertEqual(agendamento.cancelado, True)

  def test_cancelamento_sem_auth(self):
    user = create_usuario()
    create_agendamento(user)

    response = self.client.delete("/api/agendamentos/1/")
    agendamento = Agendamento.objects.get()

    self.assertEqual(response.status_code, 403)
    self.assertEqual(agendamento.cancelado, False)

class TestHorariosList(APITestCase):
  def test_dias_disponiveis(self):
    response = self.client.get("/api/agendamentos/horarios/?data_agendamento=2023-09-04")
    data = json.loads(response.content)
    date_format = '%Y-%m-%dT%H:%M:%S%z'
    first_date = datetime.strptime(data[0], date_format)
    last_date = datetime.strptime(data[-1], date_format)

    self.assertNotEqual(data, [])
    self.assertEqual(first_date, datetime(2023, 9, 4, 9, tzinfo=timezone.utc))
    self.assertEqual(last_date, datetime(2023, 9, 4, 17, 30, tzinfo=timezone.utc))

  def test_feriado(self):
    response = self.client.get("/api/agendamentos/horarios/?data_agendamento=2023-12-25")

    self.assertEqual(json.loads(response.content), [])

  @mock.patch("agenda.libs.brasil_api.is_feriado", return_value=False)
  def test_mock_dias_disponiveis(self, _):
    response = self.client.get("/api/agendamentos/horarios/?data_agendamento=2023-09-04")
    data = json.loads(response.content)
    date_format = '%Y-%m-%dT%H:%M:%S%z'
    first_date = datetime.strptime(data[0], date_format)
    last_date = datetime.strptime(data[-1], date_format)

    self.assertNotEqual(data, [])
    self.assertEqual(first_date, datetime(2023, 9, 4, 9, tzinfo=timezone.utc))
    self.assertEqual(last_date, datetime(2023, 9, 4, 17, 30, tzinfo=timezone.utc))

  @mock.patch("agenda.libs.brasil_api.is_feriado", return_value=True)
  def test_mock_feriado(self, _):
    response = self.client.get("/api/agendamentos/horarios/?data_agendamento=2023-12-25")

    self.assertEqual(json.loads(response.content), [])
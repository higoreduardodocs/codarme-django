from flask import Flask, jsonify, json, request, abort

from evento import Evento, EventoOnline


app = Flask(__name__)

evento_local = Evento("Curso de Python", "Sala 10")
evento_link = EventoOnline("Curso de Power BI")
evento_list = [evento_local, evento_link]

# ERROR HANDLERS

@app.errorhandler(400)
def handler_400(error):
  return (jsonify(error=str(error)), 400)

@app.errorhandler(404)
def handler_404(error):
  return (jsonify(error=str(error)), 404)

# ROUTES

@app.route("/hello-world/")
def index():
  return "<h1>Hello world</h1>"

@app.route("/api/eventos/")
def get_evento_list():
  eventos = []
  for evento in evento_list:
    eventos.append(evento.__dict__)
  return jsonify(eventos)

@app.route("/api/eventos/", methods=["POST"])
def post_evento_list():
  data = json.loads(request.data)
  if not data:
    abort(400, "Os campos devem ser preenchidos")

  nome = data.get("nome")
  local = data.get("local")

  if not nome:
    abort(400, "'nome' deve ser preenchido")
  if local:
    evento = Evento(nome, local)
  else:
    evento = EventoOnline(nome)
  evento_list.append(evento)
  
  return evento.__dict__

def find_evento_id(id):
  for evento in evento_list:
    if evento.id == id:
      return evento
    
  return abort(404, f"Evento id: {id} não encontrado")

@app.route("/api/eventos/<int:id>/")
def get_evento_detail(id):
  evento = find_evento_id(id)
  return jsonify(evento.__dict__)

@app.route("/api/eventos/<int:id>/", methods=["PUT"])
def put_evento_detail(id):
  data = request.get_json()
  if not data:
    abort(400, "Os campos devem ser preenchidos")

  nome = data.get("nome")
  local = data.get("local")

  if not nome:
    abort(400, "'nome' deve ser preenchido")
  if not local:
    abort(400, "'local' deve ser preenchido")

  evento = find_evento_id(id)
  evento.nome = nome
  evento.local = local
  return jsonify(evento.__dict__)

@app.route("/api/eventos/<int:id>/", methods=["PATCH"])
def patch_evento_detail(id):
  data = request.get_json()
  if not data:
    abort(400, "Algum campo deve ser preenchido")

  evento = find_evento_id(id)
  if "nome" in data.keys():
    nome = data.get("nome")
    if not nome:
      abort(400, "'nome' deve ser preenchido")
    evento.nome = nome
  if "local" in data.keys():
    local = data.get("local")
    if not local:
      abort(400, "'local' deve ser preenchido")
    evento.local = local

  return jsonify(evento.__dict__)

@app.route("/api/eventos/<int:id>/", methods=["DELETE"])
def delete_evento_detail(id):
  evento = find_evento_id(id)
  evento_list.remove(evento)
  return jsonify(id)
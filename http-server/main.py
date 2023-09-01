from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from evento import Evento, EventoOnline


evento_local = Evento("Curso de Python", "Sala 10")
evento_link = EventoOnline("Curso de Power BI")
evento_list = [evento_local, evento_link]

class SimpleHTTPHandle(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.send_header("Content-Type", "text/html; charset=utf-8")
    self.send_header("Test", "abc")
    self.end_headers()
    data = "".encode()

    if self.path == "/hello-world/":
      data = f"""
        <html>
          <head><title>Hello world</title></head>
          <body><h1>Hello world</h1></body>
        </html>
      """.encode()

    elif self.path == "/eventos/":
      evento_rows = ""
      for evento in evento_list:
        evento_rows += f"""
          <tr>
            <td>ID: {evento.id}</td>
            <td>Nome: {evento.nome}</td>
            <td>Local/Link: {evento.local}</td>
          </tr>
        """

      stylesheet = """
        <style>
          table { border-collapse: collapse; }
          td, th { border: 1px solid #ddd; text-align: left; padding: 8px; }
        </style>
      """
      data = f"""
        <html>
          <head><title>Eventos</title>{stylesheet}</head>
          <body>
            <table>
              <thead><tr>
                <th>ID</th><th>Nome</th><th>Local</th>
              </tr></thead>
              <tbody>
                {evento_rows}
              </tbody>
            </table>
          </body>
        </html>
      """.encode()

    elif self.path == "/api/eventos/":
      self.send_header("Content-Type", "application/json")
      self.end_headers()
      eventos = []
      for evento in evento_list:
        # eventos.append(evento.to_json())
        # eventos.append({
        #   "id": evento.id, "nome": evento.nome, "local": evento.local
        # })
        eventos.append(evento.__dict__)
      data = json.dumps(eventos).encode()

    self.wfile.write(data)

server = HTTPServer(('localhost', 3000), SimpleHTTPHandle)
server.serve_forever()
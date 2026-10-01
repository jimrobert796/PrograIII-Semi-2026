from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib import parse
from urllib.parse import urlparse, parse_qs
import crud_clientes
import crud_actividades

import json

port = 3000
crudClientes = crud_clientes.crud_clientes()
crudActividades = crud_actividades.crud_actividades()


class miServidor(SimpleHTTPRequestHandler):
    def responder_json(self, datos, codigo=200):
        # default=str convierte Decimal y date a texto
        cuerpo = json.dumps(datos, default=str).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_POST(self):
        longitud = int(self.headers['Content-Length'])
        datos = self.rfile.read(longitud).decode("utf-8")
        datos = parse.unquote(datos)
        datos = json.loads(datos)
        ruta = urlparse(self.path).path

        if ruta == "/cliente":
            self.responder_json({'msg': crudClientes.administrar(datos)})
        elif ruta == "/actividad":
            self.responder_json({'msg': crudActividades.administrar(datos)})
        else:
            self.responder_json({'msg': 'Ruta no encontrada'}, 404)

    def do_GET(self):
        urlParse = urlparse(self.path)
        qs = parse_qs(urlParse.query)
        ruta = urlParse.path

        if ruta == "/clientes":
            buscar = qs.get('buscar', [''])[0]
            self.responder_json(crudClientes.consultar(buscar))
        elif ruta == "/empresas":
            self.responder_json(crudActividades.empresas())
        elif ruta == "/calcular":
            balance = qs.get('balance', [''])[0]
            desde = qs.get('desde', [''])[0]
            self.responder_json(crudActividades.calcular(balance, desde))
        elif ruta == "/actividades":
            idCliente = qs.get('idCliente', [''])[0]
            self.responder_json(crudActividades.listar(idCliente))
        elif ruta == "/":
            self.path = "/index.html"  
            return SimpleHTTPRequestHandler.do_GET(self)
        else:
            self.send_error(404)


print(f"Servidor corriendo en el puerto {port}")
server = HTTPServer(("localhost", port), miServidor)
server.serve_forever()
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib import parse
from urllib.parse import urlparse, parse_qs
import crud_clientes
import crud_productos
import crud_usuarios_usss001925

import json


port = 3000
crudClientes = crud_clientes.crud_clientes()
crudProductos = crud_productos.crud_productos()
crudUsuarios = crud_usuarios_usss001925.crud_usuarios_usss001925()

class miServidor(SimpleHTTPRequestHandler):
    def do_POST(self):
        print(f"Recibiendo POST en: {self.path}")
        try:
            longitud = int(self.headers['Content-Length'])
            datos = self.rfile.read(longitud)
            datos = datos.decode("utf-8")
            datos = parse.unquote(datos)
            datos = json.loads(datos)
            print(f"Datos recibidos: {datos}")

            if datos["modulo"] == "cliente":
                respuesta = {'msg': crudClientes.administrar(datos)}
            elif datos["modulo"] == "producto":
                respuesta = {'msg': crudProductos.administrar(datos)}
            elif datos["modulo"] == "usuario":
                respuesta = {'msg': crudUsuarios.administrar(datos)}
            elif datos["modulo"] == "login":
                print("Validando login...")
                resultado = crudUsuarios.validar_login(datos.get('usuario'), datos.get('clave'))
                respuesta = {'msg': 'ok' if resultado else 'error'}
            else:
                respuesta = {'msg': 'modulo no reconocido'}
        except Exception as e:
            print(f"Error en do_POST: {e}")
            respuesta = {'msg': f'Error interno: {e}'}

        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(respuesta).encode("utf-8"))

    def do_GET(self):
        urlParse = urlparse(self.path)
        qs = parse_qs(urlParse.query)
       
        if urlParse.path == "/clientes":
            buscar = qs.get('buscar', [''])[0]
            print(buscar)
            datos = crudClientes.consultar(buscar)
            self.send_response(200)
            self.send_header("Content-type","text/json")
            self.end_headers()
            self.wfile.write(json.dumps(datos).encode("utf-8"))

        elif urlParse.path == "/productos":
            buscar = qs.get('buscar', [''])[0]
            datos = crudProductos.consultar(buscar)
            self.send_response(200)
            self.send_header("Content-type","text/json")
            self.end_headers()
            self.wfile.write(json.dumps(datos).encode("utf-8"))

        elif urlParse.path == "/usuarios":
            buscar = qs.get('buscar', [''])[0]
            datos = crudUsuarios.consultar(buscar)
            self.send_response(200)
            self.send_header("Content-type","text/json")
            self.end_headers()
            self.wfile.write(json.dumps(datos).encode("utf-8"))
        
        elif self.path == "/":
            self.path = "/login.html"
            return SimpleHTTPRequestHandler.do_GET(self)

        elif urlParse.path == "/vistas":
            self.path = f"/modulos/{qs.get('form', [''])[0]}.html"
            return SimpleHTTPRequestHandler.do_GET(self)

        else:                                              # ← AGREGAR ESTAS 2 LÍNEAS
            return SimpleHTTPRequestHandler.do_GET(self)   # ←

print(f"Servidor corriendo en el puerto {port}")
server = HTTPServer(("localhost",port),miServidor)
server.serve_forever()
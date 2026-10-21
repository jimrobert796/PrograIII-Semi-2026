from mysql.connector.errors import Error
import conexion

db = conexion.Conexion()

class crud_usuarios_usss001925:
    def consultar(self, buscar):
        # Búsqueda por nombre o usuario
        return db.consultar(f"SELECT * FROM usuarios_usss001925 WHERE nombre LIKE '%{buscar}%' OR usuario LIKE '%{buscar}%'")

    def administrar(self, datos):
        try:
            if datos['accion'] == 'nuevo':
                sql = """
                    INSERT INTO usuarios_usss001925(usuario, clave, nombre, direccion, telefono)
                    VALUES(%s, %s, %s, %s, %s)
                """
                valores = (datos['usuario'], datos['clave'], datos['nombre'], datos['direccion'], datos['telefono'])
            elif datos['accion'] == 'modificar':
                sql = """
                    UPDATE usuarios_usss001925 SET usuario=%s, clave=%s, nombre=%s, direccion=%s, telefono=%s
                    WHERE idUsuario=%s
                """
                valores = (datos['usuario'], datos['clave'], datos['nombre'], datos['direccion'], datos['telefono'], datos['idUsuario'])
            else:
                sql = """
                    DELETE FROM usuarios_usss001925 WHERE idUsuario=%s
                """
                valores = (datos['idUsuario'],)
            return db.ejecutar(sql, valores)
        except Error as e:
            return f"Error al guardar el usuario: {e}"

    def validar_login(self, usuario, clave):
        try:
            resultado = db.consultar(f"SELECT * FROM usuarios_usss001925 WHERE usuario='{usuario}' AND clave='{clave}'")
            if resultado and len(resultado) > 0:
                return True
        except Exception as e:
            print(f"Error en validar_login: {e}")
        return False

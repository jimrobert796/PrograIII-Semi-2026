import re
from datetime import date
from decimal import Decimal, InvalidOperation

import conexion
from impuestos import calcular_impuesto_municipal

db = conexion.Conexion()

ESTADO_SQL = """
    CASE
        WHEN CURDATE() >= a.desde AND CURDATE() < a.hasta THEN 'Vigente'
        WHEN a.hasta <= CURDATE() THEN 'Histórico'
        ELSE 'Futuro'
    END
"""


class crud_actividades:
    def empresas(self):
        return db.consultar(
            "SELECT idCliente, codigo, nombre FROM clientes WHERE tipo='empresa' ORDER BY nombre"
        ) or []

    def calcular(self, balance, desde=""):
        """Devuelve el precio (impuesto) o un mensaje de error."""
        try:
            d = date.fromisoformat(desde) if desde else None
            return {"msg": "ok", "precio": str(calcular_impuesto_municipal(balance, d))}
        except (ValueError, InvalidOperation) as e:
            return {"msg": str(e)}

    def listar(self, idCliente):
        sql = f"""
            SELECT a.idActividad, a.idCliente, a.codigo, a.desde, a.hasta,
                   a.balance, a.precio, {ESTADO_SQL} AS estado
            FROM actividades_economicas a
            WHERE a.idCliente = %s
            ORDER BY a.codigo, a.desde
        """
        return db.consultar(sql, (idCliente,)) or []

    def administrar(self, datos):
        accion = datos.get("accion")
        if accion == "eliminar":
            return db.ejecutar(
                "DELETE FROM actividades_economicas WHERE idActividad=%s",
                (datos.get("idActividad"),),
            )
        if accion != "nuevo":
            return "Acción no válida"

        # ---------- validaciones ----------
        idCliente = datos.get("idCliente")
        codigo = str(datos.get("codigo", "")).strip()
        if not re.fullmatch(r"[0-9]{3,10}", codigo):
            return "El código debe tener entre 3 y 10 dígitos"

        cli = db.consultar("SELECT tipo FROM clientes WHERE idCliente=%s", (idCliente,))
        if not cli:
            return "La empresa seleccionada no existe"
        if cli[0]["tipo"] != "empresa":
            return "Solo las empresas pueden registrar actividades económicas"

        try:
            desde = date.fromisoformat(datos.get("desde", ""))
            hasta = date.fromisoformat(datos.get("hasta", ""))
        except ValueError:
            return "Fechas inválidas"
        if desde >= hasta:
            return "La fecha 'Desde' debe ser anterior a 'Hasta'"

        try:
            balance = Decimal(str(datos.get("balance", "")))
        except InvalidOperation:
            return "Balance inválido"
        try:
            precio = calcular_impuesto_municipal(balance, desde)
        except ValueError as e:
            return str(e)

        # periodos superpuestos (se permite que uno termine el mismo dia que empieza otro)
        choque = db.consultar(
            """SELECT COUNT(*) AS n FROM actividades_economicas
               WHERE idCliente=%s AND codigo=%s AND desde < %s AND hasta > %s""",
            (idCliente, codigo, hasta, desde),
        )
        if choque is None:
            return "Error al validar los periodos"
        if choque[0]["n"] > 0:
            return "El periodo se superpone con otro ya registrado para esa empresa y código"

        return db.ejecutar(
            """INSERT INTO actividades_economicas(idCliente,codigo,desde,hasta,balance,precio)
               VALUES(%s,%s,%s,%s,%s,%s)""",
            (idCliente, codigo, desde, hasta, balance, precio),
        )
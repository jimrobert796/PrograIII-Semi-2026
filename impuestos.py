import math
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

# (desde, hasta, cuota_fija, tarifa_por_millar)
_TRAMOS = [
    ("0.01",       "500.00",     "1.50",   "0.00"),
    ("500.01",     "1000.00",    "1.50",   "3.00"),
    ("1000.01",    "2000.00",    "3.00",   "3.00"),
    ("2000.01",    "3000.00",    "6.00",   "3.00"),
    ("3000.01",    "6000.00",    "9.00",   "2.00"),
    ("8000.01",    "18000.00",   "15.00",  "2.00"),
    ("18000.01",   "30000.00",   "39.00",  "2.00"),
    ("30000.01",   "60000.00",   "63.00",  "1.00"),
    ("60000.01",   "100000.00",  "93.00",  "0.80"),
    ("100000.01",  "200000.00",  "125.00", "0.70"),
    ("200000.01",  "300000.00",  "195.00", "0.60"),
    ("300000.01",  "400000.00",  "255.00", "0.45"),
    ("400000.01",  "500000.00",  "300.00", "0.40"),
    ("500000.01",  "1000000.00", "340.00", "0.30"),
    ("1000000.01", "Infinity",   "490.00", "0.18"),
]
TRAMOS = [tuple(Decimal(x) for x in t) for t in _TRAMOS]
CENTAVO = Decimal("0.01")

# La regla de calculo cambia segun la fecha "Desde" del periodo (tarifa versionada):
#   - periodos que empiezan ANTES de esta fecha: excedente proporcional  (700 -> 2.10)
#   - periodos desde esta fecha en adelante:     millares completos o fraccion (545/550 -> 4.50)
# Esto se deduce del ejemplo de periodos historicos; confirmar con la ordenanza/docente.
FECHA_CAMBIO_REGLA = date(2023, 1, 1)


def calcular_impuesto_municipal(balance, desde=None):
    """Impuesto = cuota fija + excedente x tarifa por millar.
    desde (date, opcional): inicio del periodo; decide que regla de excedente aplica."""
    balance = Decimal(str(balance))
    if balance <= 0:
        raise ValueError("El balance debe ser mayor que 0")
    proporcional = desde is not None and desde < FECHA_CAMBIO_REGLA

    for inf, sup, cuota, tarifa in TRAMOS:
        if balance <= sup:
            if balance <= inf - CENTAVO:
                raise ValueError(f"No existe tarifa para el balance {balance}")
            if tarifa == 0:
                return cuota.quantize(CENTAVO)
            if proporcional:
                millares = (balance - (inf - CENTAVO)) / 1000
            else:
                millares = math.ceil((balance - inf) / 1000)
            return (cuota + millares * tarifa).quantize(CENTAVO, ROUND_HALF_UP)
    raise ValueError(f"No existe tarifa para el balance {balance}")


if __name__ == "__main__":
    ejemplo = [
        (date(2022, 1, 1), 700), (date(2023, 1, 1), 545), (date(2024, 1, 1), 550),
        (date(2025, 1, 1), 550), (date(2026, 1, 1), 550),
    ]
    total = Decimal("0")
    for d, b in ejemplo:
        p = calcular_impuesto_municipal(b, d)
        total += p
        print(d, b, p)
    print("Total historico:", total)   # 20.10
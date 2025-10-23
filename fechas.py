"""Puente de fechas para el IDE.

Ofrece utilidades mínimas compatibles con la app.
"""
from __future__ import annotations
from datetime import datetime


def dias_faltantes(fecha_texto: str) -> int:
    try:
        dd, mm, aaaa = fecha_texto.replace('-', '/').split('/')
        dt = datetime(int(aaaa), int(mm), int(dd))
    except Exception:
        return 0
    return (dt - datetime.now()).days


def estado_por_dias(fecha_texto: str) -> str:
    d = dias_faltantes(fecha_texto)
    if d < 0:
        return 'VENCIDO'
    if d == 0:
        return 'HOY'
    if d <= 3:
        return 'PRONTO'
    return 'A TIEMPO'


def formatear_fecha(fecha_texto: str) -> str:
    try:
        dd, mm, aaaa = fecha_texto.replace('-', '/').split('/')
        return f"{int(dd):02d}/{int(mm):02d}/{int(aaaa):04d}"
    except Exception:
        return fecha_texto

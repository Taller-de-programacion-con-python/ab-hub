"""Puente de mensajes para el IDE.

Provee las funciones `mostrar_mensaje_exito`, `mostrar_mensaje_error` y
`mostrar_mensaje_info` para que el import resuelva sin advertencias.
En tiempo de ejecución devuelven el texto recibido.
"""
from __future__ import annotations

from typing import Any


def mostrar_mensaje_exito(texto: Any) -> str:
    return str(texto)


def mostrar_mensaje_error(texto: Any) -> str:
    return str(texto)


def mostrar_mensaje_info(texto: Any) -> str:
    return str(texto)


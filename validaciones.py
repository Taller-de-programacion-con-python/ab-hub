"""Puente de validaciones para el IDE.

Replica las funciones usadas en la app para eliminar warnings de import.
"""
from __future__ import annotations


def es_texto_vacio(texto) -> bool:
    if texto is None:
        return True
    return str(texto).strip() == ""


def es_correo_valido(correo) -> bool:
    if correo is None:
        return False
    correo = str(correo)
    if "@" not in correo:
        return False
    usuario, _, dominio = correo.partition("@")
    return bool(usuario) and "." in dominio


def es_contrasena_valida(contrasena) -> bool:
    if contrasena is None:
        return False
    contrasena = str(contrasena)
    if len(contrasena) < 8:
        return False
    tiene_letra = any(c.isalpha() for c in contrasena)
    tiene_numero = any(c.isdigit() for c in contrasena)
    return tiene_letra and tiene_numero

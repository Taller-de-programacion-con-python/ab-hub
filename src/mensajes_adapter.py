"""
Adaptador de mensajes para 3°.

- Si el paquete `mensajes` (de 1°) está disponible, usa sus claves y su función t().
- Si no, usa un FALBACK local con las claves mínimas para la demo/CLI.

Uso:
    from mensajes_adapter import t

    ok, msg = login(email, password)        # msg viene de t("auth_ok") o t("auth_fail")
    print(t("task_list_header"))
"""

from typing import Dict, Tuple, List

_T_EXTERN = None
_CATALOGO: Dict[str, str] = {}

try:
    from mensajes import t as _T_EXTERN, MENSAJES as _CATALOGO
except Exception:
    _CATALOGO = {
        "auth_ok": "Inicio de sesión correcto",
        "auth_fail": "Usuario o contraseña no válidos",
        "user_exists": "El usuario ya existe",
        "invalid_input": "Datos incompletos o inválidos",

        "task_added": "Tarea agregada",
        "task_updated": "Tarea actualizada",
        "task_marked_done": "Tarea marcada como hecha",
        "task_not_found": "No se encontró la tarea",
        "task_list_header": "Tus tareas:",

        "unexpected_error": "Ocurrió un error inesperado",
        "db_error": "Error de base de datos",
        "due_date_invalid": "La fecha no es válida (usa DD/MM)",
        "password_weak": "La contraseña es débil",
    }

    def _T_EXTERN(clave: str, **kv) -> str:
        base = _CATALOGO.get(clave, clave)
        try:
            return base.format(**kv) if kv else base
        except Exception:
            return base


def t(clave: str, **kv) -> str:
    """
    Devuelve el texto asociado a `clave`. Soporta placeholders con **kv.
    Ej: t("task_added"); t("greeting", nombre="Ana") -> "Hola Ana"
    """
    try:
        return _T_EXTERN(clave, **kv)
    except Exception:
        base = _CATALOGO.get(clave, clave)
        try:
            return base.format(**kv) if kv else base
        except Exception:
            return base


def keys() -> List[str]:
    """Lista de claves de mensaje disponibles."""
    return list(_CATALOGO.keys())


def has_key(clave: str) -> bool:
    """True si la clave existe en el catálogo actual."""
    return clave in _CATALOGO


def ensure(required: List[str]) -> Tuple[bool, List[str]]:
    """
    Verifica que existan todas las claves requeridas.
    Retorna (ok, faltantes).
    """
    faltantes = [k for k in required if k not in _CATALOGO]
    return (len(faltantes) == 0, faltantes)

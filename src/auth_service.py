from hashlib import sha256
from uuid import uuid4
from db import get_conn
from mensajes_adapter import t 

def hash_password(password: str) -> str:
    """Genera una cadena 'salt$hash' segura para guardar en la base de datos."""
    salt = uuid4().hex
    digest = sha256((salt + password).encode()).hexdigest()
    return f"{salt}${digest}"

def verify_password(password: str, stored: str) -> bool:
    """Verifica una contraseña ingresada contra el hash almacenado."""
    try:
        salt, digest = stored.split("$")
        return sha256((salt + password).encode()).hexdigest() == digest
    except Exception:
        return False



def registrar_usuario(correo: str, contrasena: str, nombre: str = ""):
    correo = correo.strip().lower()
    try:
        with get_conn() as con:
            existe = con.execute(
                "SELECT 1 FROM usuarios WHERE correo = ?", (correo,)
            ).fetchone()
            if existe:
                return False, t("user_exists")

            contrasena_hash = hash_password(contrasena)
            con.execute(
                "INSERT INTO usuarios(correo, contrasena, nombre) VALUES(?,?,?)",
                (correo, contrasena_hash, nombre),
            )
        return True, t("auth_ok")
    except Exception as e:
        print("Error en registrar_usuario:", e)
        return False, t("invalid_input")


def login(correo: str, contrasena: str):
    correo = correo.strip().lower()
    try:
        with get_conn() as con:
            row = con.execute(
                "SELECT contrasena FROM usuarios WHERE correo=?",
                (correo,),
            ).fetchone()

        if not row:
            return False, t("auth_fail")

        stored_hash = row["contrasena"]
        if verify_password(contrasena, stored_hash) or stored_hash == contrasena:
            return True, t("auth_ok")
        else:
            return False, t("auth_fail")

    except Exception as e:
        print("Error en login:", e)
        return False, t("invalid_input")

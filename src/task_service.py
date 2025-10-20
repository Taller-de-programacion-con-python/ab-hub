from db import get_conn

def agregar_tarea(correo: str, texto: str, fecha_ddmm: str) -> bool:
    correo, texto, fecha_ddmm = correo.strip().lower(), texto.strip(), fecha_ddmm.strip()
    if not correo or not texto or not fecha_ddmm:
        return False
    try:
        with get_conn() as con:
            con.execute(
                "INSERT INTO tasks(usuario, texto, fecha, done) VALUES(?,?,?,0)",
                (correo, texto, fecha_ddmm)
            )
        return True
    except Exception:
        return False

def listar_tareas(correo: str):
    correo = correo.strip().lower()
    with get_conn() as con:
        return con.execute(
            "SELECT id, texto, fecha, done FROM tasks WHERE usuario=? ORDER BY id DESC",
            (correo,)
        ).fetchall()
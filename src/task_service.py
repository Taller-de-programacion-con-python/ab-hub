from db import get_conn

def agregar_tarea(correo: str, texto: str, fecha_ddmm: str, done: bool = False) -> bool:
    correo, texto, fecha_ddmm = correo.strip().lower(), texto.strip(), fecha_ddmm.strip()
    if not correo or not texto or not fecha_ddmm:
        return False
    try:
        with get_conn() as con:
            con.execute(
                "INSERT INTO tasks(usuario, texto, fecha, done) VALUES(?,?,?,?)",
                (correo, texto, fecha_ddmm, int(bool(done))),
            )
        return True
    except Exception:
        return False

def actualizar_tarea(correo: str, tarea_id: int, texto: str, fecha_ddmm: str, done: bool) -> bool:
    correo, texto = correo.strip().lower(), texto.strip()
    fecha_ddmm = fecha_ddmm.strip()
    if not correo or not tarea_id or not texto:
        return False
    try:
        with get_conn() as con:
            cursor = con.execute(
                "UPDATE tasks SET texto=?, fecha=?, done=? WHERE id=? AND usuario=?",
                (texto, fecha_ddmm, int(bool(done)), tarea_id, correo),
            )
        return cursor.rowcount > 0
    except Exception:
        return False

def listar_tareas(correo: str):
    correo = correo.strip().lower()
    with get_conn() as con:
        return con.execute(
            "SELECT id, texto, fecha, done FROM tasks WHERE usuario=? ORDER BY id DESC",
            (correo,)
        ).fetchall()

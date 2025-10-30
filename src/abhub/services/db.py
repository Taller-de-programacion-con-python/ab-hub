import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def _db_path() -> Path:
    # Prefer a bloc.db next to this module; fallback to src/bloc.db
    candidates = [
        BASE_DIR / "bloc.db",
        BASE_DIR.parent.parent / "bloc.db",  # src/bloc.db
    ]
    for p in candidates:
        if p.exists():
            return p
    return candidates[0]


DB_PATH = _db_path()


def get_conn():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

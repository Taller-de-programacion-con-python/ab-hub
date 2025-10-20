import sqlite3, pathlib

DB_PATH = pathlib.Path(__file__).with_name("bloc.db")

def get_conn():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

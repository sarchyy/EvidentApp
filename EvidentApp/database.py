
import sqlite3

def get_db_connection():
    con = sqlite3.connect('db.db')
    con.row_factory = sqlite3.Row
    return con

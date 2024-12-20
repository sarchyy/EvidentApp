import sqlite3

def update_table():
    con = sqlite3.connect('db.db')
    cur = con.cursor()

 
    cur.execute("PRAGMA table_info(employees)")
    columns = [column[1] for column in cur.fetchall()]

    if 'start_time' not in columns:
        cur.execute("ALTER TABLE employees ADD COLUMN start_time TEXT")
    
    if 'end_time' not in columns:
        cur.execute("ALTER TABLE employees ADD COLUMN end_time TEXT")
    
    con.commit()
    con.close()

update_table()

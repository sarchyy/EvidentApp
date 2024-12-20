import sqlite3

def create_tables():
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    
   
    cur.execute(''' 
        CREATE TABLE IF NOT EXISTS employees (
            rowid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            wh REAL NOT NULL
        )
    ''')

 
    cur.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    ''')

    cur.execute(''' 
        CREATE TABLE IF NOT EXISTS travel_orders (
            rowid INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT NOT NULL,
            destination TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            purpose TEXT NOT NULL,
            daily_allowance REAL NOT NULL,
            advance_payment REAL NOT NULL,
            contact_info TEXT NOT NULL,
            transportation_mode TEXT NOT NULL,
            departure_time TEXT NOT NULL,
            return_time TEXT NOT NULL
        )
    ''')

    con.commit()
    con.close()

create_tables()

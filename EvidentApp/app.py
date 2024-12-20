
from flask import Flask, make_response, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
import os
from weasyprint import HTML

from database import get_db_connection



app = Flask(__name__)
app.secret_key = 'secret123'
app.permanent_session_lifetime = timedelta(days=7)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            return "Pristup odbijen", 403
        return f(*args, **kwargs)
    return decorated_function
@app.route('/routes')
def show_routes():
    return str(app.url_map)

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/enternew")
def enternew():
    return render_template("employee.html")

@app.route("/addrec", methods=['POST'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            date = request.form['date']
            start_time = request.form['start_time']
            end_time = request.form['end_time']
            
            if not (nm and date and start_time and end_time):
                return "Svi podaci moraju biti ispunjeni.", 400
            
            start_dt = datetime.strptime(start_time, "%H:%M")
            end_dt = datetime.strptime(end_time, "%H:%M")
            
            worked_hours = (end_dt - start_dt).seconds / 3600
            
            with get_db_connection() as con:
                cur = con.cursor()
                cur.execute("INSERT INTO employees (name, date, start_time, end_time, wh) VALUES (?,?,?,?,?)",
                            (nm, date, start_time, end_time, worked_hours))
                con.commit()
                msg = "Zapis uspješno dodan u bazu podataka"
        except sqlite3.Error as e:
            msg = f"Greška pri dodavanju zapisa: {e}"
        return render_template('result.html', msg=msg)

@app.route('/list', methods=['GET', 'POST'])
def list_employees():
    con = get_db_connection()
    cur = con.cursor()

    query = "SELECT rowid, * FROM employees"
    filters = []

    name_filter = request.form.get('name_filter', '')
    date_filter = request.form.get('date_filter', '')

    if name_filter:
        filters.append("name LIKE ?")
    if date_filter:
        filters.append("date = ?")

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += " ORDER BY date DESC"

    params = []
    if name_filter:
        params.append(f"%{name_filter}%")
    if date_filter:
        params.append(date_filter)

    cur.execute(query, params)
    rows = cur.fetchall()
    con.close()
    return render_template("list.html", rows=rows, name_filter=name_filter, date_filter=date_filter)

@app.route("/delete", methods=['POST'])
@admin_required
def delete():
    if request.method == 'POST':
        try:
            rowid = request.form['id']
            with get_db_connection() as con:
                cur = con.cursor()
                cur.execute("DELETE FROM employees WHERE rowid=?", (rowid,))
                con.commit()
                msg = "Zapis uspješno obrisan iz baze podataka"
        except sqlite3.Error as e:
            msg = f"Greška pri brisanju: {e}"
        return render_template('result.html', msg=msg)


@app.route("/reset_password", methods=['POST'])
def reset_password():
    email = request.form['email']
    return render_template('result.html', msg="Link za resetiranje lozinke poslan na vaš e-mail")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'user') 
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        try:
            with sqlite3.connect('db.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, role))
                con.commit()
                msg = f"Korisnik {username} uspješno registriran!"
        except sqlite3.Error as e:
            msg = f"Greška u registraciji: {e}"
        return render_template('result.html', msg=msg)
    return render_template('register.html')
@app.route('/travel_orders')
def travel_orders():
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM travel_orders")
    orders = cur.fetchall()
    con.close()
    return render_template('travel_orders.html', orders=orders)


@app.route('/travel_order/<int:rowid>')
def travel_order(rowid):
    try:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute('SELECT * FROM travel_orders WHERE rowid = ?', (rowid,))
        order = cur.fetchone()
        con.close()

        if order:
            return render_template('travel_order_template.html',
                                   employee_name=order['employee_name'],
                                   job_title=order['job_title'],
                                   issue_date=order['issue_date'],
                                   destination=order['destination'],
                                   start_date=order['start_date'],
                                   end_date=order['end_date'],
                                   departure_time=order['departure_time'],
                                   arrival_time=order['arrival_time'],
                                   purpose=order['purpose'],
                                   daily_allowance=order['daily_allowance'],
                                   advance_payment=order['advance_payment'])
        else:
            return "Putni nalog nije pronađen.", 404

    except sqlite3.Error as e:
        return f"Greška u bazi podataka: {e}", 500




@app.route('/add_travel_order', methods=['GET', 'POST'])
def add_travel_order():
    if request.method == 'POST':
    
        employee_name = request.form['employee_name']
        destination = request.form['destination']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        purpose = request.form['purpose']
        daily_allowance = request.form.get('daily_allowance', 0)
        advance_payment = request.form.get('advance_payment', 0)
        contact_info = request.form.get('contact_info', '')
        transportation_mode = request.form.get('transportation_mode', '')
        departure_time = request.form.get('departure_time', '')
        return_time = request.form.get('return_time', '')

        if not all([employee_name, destination, start_date, end_date, purpose]):
            return "Sva obavezna polja moraju biti popunjena!", 400

        try:
            with get_db_connection() as con:
                cur = con.cursor()
                cur.execute('''
                    INSERT INTO travel_orders 
                    (employee_name, destination, start_date, end_date, purpose, 
                     daily_allowance, advance_payment, contact_info, 
                     transportation_mode, departure_time, return_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (employee_name, destination, start_date, end_date, purpose, 
                      daily_allowance, advance_payment, contact_info, 
                      transportation_mode, departure_time, return_time))
                con.commit()
            return redirect('/travel_orders')
        except sqlite3.Error as e:
            return f"Greška pri unosu podataka: {e}", 500

    return render_template('add_travel_order.html')



@app.route('/delete_travel_order/<int:rowid>', methods=['POST'])
@admin_required
def delete_travel_order(rowid):
    try:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute('DELETE FROM travel_orders WHERE rowid = ?', (rowid,))
        con.commit()
        con.close()
    except sqlite3.Error as e:
        return f"Greška pri brisanju: {e}", 500
    return redirect(url_for('travel_orders'))

import os
from datetime import datetime

def update_tables():
    try:
        with sqlite3.connect('db.db') as con:
            cur = con.cursor()
            
       
            cur.execute("DROP TABLE IF EXISTS travel_orders")
        
            cur.execute("ALTER TABLE travel_orders2 RENAME TO travel_orders")
            
            con.commit()
            print("Tabela je uspešno ažurirana.")
    except sqlite3.Error as e:
        print(f"Greška: {e}")
        
        
@app.route('/travel_order_pdf/<int:id>', methods=['GET'])
def generate_pdf(id):
    try:
        con = get_db_connection()
        con.row_factory = sqlite3.Row  
        cur = con.cursor()
        cur.execute('SELECT * FROM travel_orders WHERE rowid = ?', (id,))
        row = cur.fetchone()

        if not row:
            return "Putni nalog nije pronađen", 404

        row = dict(row)  

        html_content = render_template(
            'travel_order_template.html',
            employee_name=row.get('employee_name', 'N/A'),
            destination=row.get('destination', 'N/A'),
            start_date=row.get('start_date', 'N/A'),
            end_date=row.get('end_date', 'N/A'),
            purpose=row.get('purpose', 'N/A'),
            daily_allowance=row.get('daily_allowance', '0.00'),
            advance_payment=row.get('advance_payment', '0.00'),
            contact_info=row.get('contact_info', 'N/A'),
            transportation_mode=row.get('transportation_mode', 'N/A'),
            departure_time=row.get('departure_time', 'N/A'),
            return_time=row.get('return_time', 'N/A')
        )

        folder_path = os.path.join(os.path.dirname(__file__), 'pdfs')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        pdf_file_path = os.path.join(folder_path, f"output_{id}.pdf")
        HTML(string=html_content).write_pdf(target=pdf_file_path)

        return f"PDF dokument uspješno spremljen u: {pdf_file_path}"

    except Exception as e:
        return f"Greška: {e}", 500


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()
        con.close()
        
        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('home'))
        else:
            return "Neispravni podaci, pokušajte ponovo.", 403
    
    return render_template("login.html")
@app.route('/travel_order', methods=['GET'])
def show_travel_order_form():
    return render_template('add_travel_order.html')  


@app.route('/travel_order', methods=['POST'])
def handle_travel_order_submission():
 
    employee_name = request.form['employee_name']
    destination = request.form['destination']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    purpose = request.form['purpose']
    daily_allowance = request.form.get('daily_allowance', 0)
    advance_payment = request.form.get('advance_payment', 0)
    contact_info = request.form.get('contact_info', '')
    transportation_mode = request.form.get('transportation_mode', '')
    departure_time = request.form.get('departure_time', '')
    return_time = request.form.get('return_time', '')

  
    if not all([employee_name, destination, start_date, end_date, purpose]):
        return "Sva obavezna polja moraju biti popunjena!", 400

    try:
     
        with get_db_connection() as con:
            cur = con.cursor()
            cur.execute('''INSERT INTO travel_orders 
                           (employee_name, destination, start_date, end_date, purpose, 
                            daily_allowance, advance_payment, contact_info, 
                            transportation_mode, departure_time, return_time) 
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                        (employee_name, destination, start_date, end_date, purpose, 
                         daily_allowance, advance_payment, contact_info, 
                         transportation_mode, departure_time, return_time))
            con.commit()
        return "Putni nalog uspješno zaprimljen!"
    except sqlite3.Error as e:
        return f"Greška pri unosu podataka: {e}", 500


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
       
        flash("Link za resetiranje lozinke poslan je na email.")
        return redirect(url_for('login'))
    return render_template('forgot_password.html')

 
def alter_travel_orders_table():
  
    conn = sqlite3.connect('db.db')  
    cursor = conn.cursor()

   
    try:
        cursor.execute("ALTER TABLE travel_orders ADD COLUMN contact_info TEXT")
    except sqlite3.OperationalError:
        print("Kolona 'contact_info' već postoji.")

    try:
        cursor.execute("ALTER TABLE travel_orders ADD COLUMN transportation_mode TEXT")
    except sqlite3.OperationalError:
        print("Kolona 'transportation_mode' već postoji.")

    try:
        cursor.execute("ALTER TABLE travel_orders ADD COLUMN departure_time TEXT")
    except sqlite3.OperationalError:
        print("Kolona 'departure_time' već postoji.")

    try:
        cursor.execute("ALTER TABLE travel_orders ADD COLUMN return_time TEXT")
    except sqlite3.OperationalError:
        print("Kolona 'return_time' već postoji.")

  
    conn.commit()
    conn.close()
    
    
@app.route('/summary')
def summary():
    try:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT name, SUM(wh) as total_hours FROM employees GROUP BY name")
        rows = cur.fetchall()
        con.close()
        return render_template("summary.html", rows=rows)
    except sqlite3.Error as e:
        return f"Došlo je do greške: {e}"
if __name__ == "__main__":
    app.run(debug=True)

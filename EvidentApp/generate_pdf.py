from flask import Flask, render_template, make_response
from weasyprint import HTML
from database import get_db_connection

app = Flask(__name__)

@app.route('/travel_order_pdf/<int:id>', methods=['GET'])
def generate_pdf(id):
    try:
       
        con = get_db_connection()
        cur = con.cursor()
        cur.execute('SELECT * FROM travel_orders WHERE rowid = ?', (id,))
        row = cur.fetchone()
        con.close()

        if not row:
            return "Putni nalog nije pronađen", 404

     
        html_content = render_template(
            'travel_order_template.html',
            employee_name=row['employee_name'],
            destination=row['destination'],
            start_date=row['start_date'],
            end_date=row['end_date'],
            purpose=row['purpose'],
            daily_allowance=row['daily_allowance'],
            advance_payment=row['advance_payment'],
            contact_info=row.get('contact_info', ''),  
            transportation_mode=row.get('transportation_mode', ''),
            departure_time=row.get('departure_time', ''),
            return_time=row.get('return_time', '')
        )

    
        pdf = HTML(string=html_content).write_pdf()

    
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename=output{id}.pdf'
        return response

    except Exception as e:
        return f"Greška: {e}", 500

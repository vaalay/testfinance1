from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
DB = 'gestiune_clienti.db'

# -------------------- CONEXIUNE DB --------------------
def get_db_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# -------------------- INDEX --------------------
@app.route('/')
def index():
    return redirect(url_for('clients'))

# -------------------- CLIENTI --------------------
@app.route('/clients')
def clients():
    conn = get_db_connection()
    clienti_list = conn.execute('SELECT * FROM clienti').fetchall()
    conn.close()
    return render_template('clients.html', clienti=clienti_list)

@app.route('/clients/add', methods=('GET', 'POST'))
def add_client():
    if request.method == 'POST':
        data = (
            request.form['nume'], 
            request.form['prenume'], 
            request.form.get('email', ''),
            request.form.get('telefon', ''), 
            request.form.get('adresa', ''), 
            request.form.get('data_nastere', ''),
            request.form.get('stare_civila', ''), 
            request.form.get('cnp', ''), 
            request.form.get('serie_buletin', ''),
            request.form.get('numar_buletin', ''), 
            request.form.get('eliberat_de', ''), 
            request.form.get('angajator', ''),
            request.form.get('detalii_angajator', ''), 
            request.form.get('info_aditionale', '')
        )
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO clienti (nume, prenume, email, telefon, adresa, data_nastere, stare_civila,
                                 cnp, serie_buletin, numar_buletin, eliberat_de, angajator,
                                 detalii_angajator, info_aditionale)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        conn.commit()
        conn.close()
        return redirect(url_for('clients'))
    return render_template('add_client.html', client=None)

@app.route('/clients/edit/<int:id>', methods=('GET', 'POST'))
def edit_client(id):
    conn = get_db_connection()
    client = conn.execute('SELECT * FROM clienti WHERE id=?', (id,)).fetchone()
    if request.method == 'POST':
        data = (
            request.form['nume'], 
            request.form['prenume'], 
            request.form.get('email', ''),
            request.form.get('telefon', ''), 
            request.form.get('adresa', ''), 
            request.form.get('data_nastere', ''),
            request.form.get('stare_civila', ''), 
            request.form.get('cnp', ''), 
            request.form.get('serie_buletin', ''),
            request.form.get('numar_buletin', ''), 
            request.form.get('eliberat_de', ''), 
            request.form.get('angajator', ''),
            request.form.get('detalii_angajator', ''), 
            request.form.get('info_aditionale', ''), 
            id
        )
        conn.execute('''
            UPDATE clienti SET
            nume=?, prenume=?, email=?, telefon=?, adresa=?, data_nastere=?, stare_civila=?,
            cnp=?, serie_buletin=?, numar_buletin=?, eliberat_de=?, angajator=?, detalii_angajator=?,
            info_aditionale=? WHERE id=?
        ''', data)
        conn.commit()
        conn.close()
        return redirect(url_for('clients'))
    conn.close()
    return render_template('add_client.html', client=client)

@app.route('/clients/delete/<int:id>', methods=('POST',))
def delete_client(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM clienti WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('clients'))

# -------------------- CREDITE --------------------
@app.route('/credits')
def credits():
    conn = get_db_connection()
    credite_list = conn.execute('''
        SELECT credite.*, clienti.nume, clienti.prenume
        FROM credite
        JOIN clienti ON credite.id_client = clienti.id
    ''').fetchall()
    conn.close()
    return render_template('credits.html', credite=credite_list)

@app.route('/credits/add', methods=('GET', 'POST'))
def add_credit():
    conn = get_db_connection()
    clienti_list = conn.execute('SELECT * FROM clienti').fetchall()
    if request.method == 'POST':
        data = (
            request.form['id_client'], 
            request.form['suma'], 
            request.form.get('dobanda', 0),
            request.form.get('com_adm', 0), 
            request.form.get('dobanda_maj', 0),
            request.form.get('perioada', 0), 
            request.form['data_inceput'], 
            request.form['data_sfarsit'],
            request.form.get('status', 'Acordat')
        )
        conn.execute('''
            INSERT INTO credite (id_client, suma, dobanda, com_adm, dobanda_maj, perioada,
                                 data_inceput, data_sfarsit, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        conn.commit()
        conn.close()
        return redirect(url_for('credits'))
    conn.close()
    return render_template('add_credit.html', credit=None, clienti=clienti_list)

@app.route('/credits/edit/<int:id>', methods=('GET', 'POST'))
def edit_credit(id):
    conn = get_db_connection()
    credit = conn.execute('SELECT * FROM credite WHERE id=?', (id,)).fetchone()
    clienti_list = conn.execute('SELECT * FROM clienti').fetchall()
    if request.method == 'POST':
        data = (
            request.form['id_client'], 
            request.form['suma'], 
            request.form.get('dobanda', 0),
            request.form.get('com_adm', 0), 
            request.form.get('dobanda_maj', 0),
            request.form.get('perioada', 0), 
            request.form['data_inceput'], 
            request.form['data_sfarsit'],
            request.form.get('status', 'Acordat'), 
            id
        )
        conn.execute('''
            UPDATE credite SET id_client=?, suma=?, dobanda=?, com_adm=?, dobanda_maj=?, perioada=?,
            data_inceput=?, data_sfarsit=?, status=? WHERE id=?
        ''', data)
        conn.commit()
        conn.close()
        return redirect(url_for('credits'))
    conn.close()
    return render_template('add_credit.html', credit=credit, clienti=clienti_list)

@app.route('/credits/delete/<int:id>', methods=('POST',))
def delete_credit(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM credite WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('credits'))

@app.route('/credits/detalii/<int:id>')
def credit_detalii(id):
    conn = get_db_connection()
    credit = conn.execute('''
        SELECT credite.*, clienti.nume, clienti.prenume
        FROM credite
        JOIN clienti ON credite.id_client = clienti.id
        WHERE credite.id=?
    ''', (id,)).fetchone()
    
    # Generare scadentar simplu
    scadentar = []
    if credit:
        suma = float(credit['suma'])
        perioada = int(credit['perioada']) if credit['perioada'] else 12
        dobanda_lunara = float(credit['dobanda']) if credit['dobanda'] else 0
        comision = float(credit['com_adm']) if credit['com_adm'] else 0
        
        rata_capital = suma / perioada
        sold = suma
        
        data_start = datetime.strptime(credit['data_inceput'], '%Y-%m-%d')
        
        for i in range(1, perioada + 1):
            val_dobanda = sold * (dobanda_lunara / 100)
            val_comision = suma * (comision / 100)
            total_rata = rata_capital + val_dobanda + val_comision
            sold -= rata_capital
            
            data_scadenta = data_start + timedelta(days=30*i)
            
            scadentar.append({
                'nr_scadenta': i,
                'data_scadenta': data_scadenta.strftime('%Y-%m-%d'),
                'val_principal': round(rata_capital, 2),
                'val_dobanda': round(val_dobanda, 2),
                'val_comision': round(val_comision, 2),
                'total_rata': round(total_rata, 2),
                'sold': round(sold, 2)
            })
    
    conn.close()
    return render_template('credit_detalii.html', credit=credit, scadentar=scadentar)

# -------------------- CONTURI --------------------
@app.route('/accounts')
def accounts():
    conn = get_db_connection()
    conturi_list = conn.execute('SELECT * FROM conturi').fetchall()
    conn.close()
    return render_template('accounts.html', conturi=conturi_list)

@app.route('/accounts/add', methods=('GET', 'POST'))
def add_account():
    if request.method == 'POST':
        data = (
            request.form['cod_cont'], 
            request.form['nume_cont'], 
            request.form['tip_cont'],
            request.form.get('sold_debitor', 0), 
            request.form.get('sold_creditor', 0),
            request.form.get('status_cont', 'activ')
        )
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO conturi (cod_cont, nume_cont, tip_cont, sold_debitor, sold_creditor, status_cont)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', data)
        conn.commit()
        conn.close()
        return redirect(url_for('accounts'))
    return render_template('add_account.html', cont=None)

@app.route('/accounts/edit/<int:id>', methods=('GET', 'POST'))
def edit_account(id):
    conn = get_db_connection()
    cont = conn.execute('SELECT * FROM conturi WHERE id=?', (id,)).fetchone()
    if request.method == 'POST':
        data = (
            request.form['cod_cont'], 
            request.form['nume_cont'], 
            request.form['tip_cont'],
            request.form.get('sold_debitor', 0), 
            request.form.get('sold_creditor', 0),
            request.form.get('status_cont', 'activ'), 
            id
        )
        conn.execute('''
            UPDATE conturi SET cod_cont=?, nume_cont=?, tip_cont=?, sold_debitor=?, sold_creditor=?, status_cont=?
            WHERE id=?
        ''', data)
        conn.commit()
        conn.close()
        return redirect(url_for('accounts'))
    conn.close()
    return render_template('add_account.html', cont=cont)

@app.route('/accounts/delete/<int:id>', methods=('POST',))
def delete_account(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM conturi WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('accounts'))

# -------------------- CONFIGURARE CREDITE --------------------
@app.route('/config_credit')
def config_credit():
    conn = get_db_connection()
    config_list = conn.execute('SELECT * FROM config_credite').fetchall()
    conn.close()
    return render_template('config_credit.html', configs=config_list)

@app.route('/config_credit/add', methods=('GET','POST'))
def add_config_credit():
    if request.method == 'POST':
        data = (
            request.form['tip_credit'], 
            request.form['dobanda'], 
            request.form['com_adm'],
            request.form['com_dosar'], 
            request.form['dobanda_maj'], 
            request.form['perioada_luni']
        )
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO config_credite (tip_credit, dobanda, com_adm, com_dosar, dobanda_maj, perioada_luni)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', data)
        conn.commit()
        conn.close()
        return redirect(url_for('config_credit'))
    return render_template('add_config_credit.html')

# -------------------- INCHIDERE ZI --------------------
@app.route('/inchidere_zi')
def inchidere_zi():
    data_selectata = request.args.get('data', datetime.now().strftime('%Y-%m-%d'))
    
    conn = get_db_connection()
    
    try:
        # Obține credite - verificăm dacă există coloana status
        credite = conn.execute('''
            SELECT clienti.nume, clienti.prenume, credite.id as nr_contract,
                   COALESCE(credite.status, 'Necunoscut') as status, 
                   credite.suma as suma_imprumutata, 0 as restanta
            FROM credite
            JOIN clienti ON credite.id_client = clienti.id
            WHERE credite.data_inceput <= ?
        ''', (data_selectata,)).fetchall()
    except sqlite3.OperationalError as e:
        # Dacă coloana status nu există, folosim o valoare default
        print(f"Eroare la interogare: {e}")
        credite = conn.execute('''
            SELECT clienti.nume, clienti.prenume, credite.id as nr_contract,
                   'Activ' as status,
                   credite.suma as suma_imprumutata, 0 as restanta
            FROM credite
            JOIN clienti ON credite.id_client = clienti.id
            WHERE credite.data_inceput <= ?
        ''', (data_selectata,)).fetchall()
    
    # Simulare incasari (pentru ca nu ai tabel de incasari complet)
    incasari = []
    
    total_credite = sum([float(c['suma_imprumutata']) if c['suma_imprumutata'] else 0 for c in credite])
    total_incasari = 0
    total_restant = 0
    
    conn.close()
    
    raport = {
        'data': data_selectata,
        'credite': credite,
        'incasari': incasari,
        'total_credite': round(total_credite, 2),
        'total_incasari': total_incasari,
        'total_restant': total_restant
    }
    
    return render_template('inchidere_zi.html', raport=raport)

# -------------------- RUN --------------------
if __name__ == '__main__':
    app.run(debug=True)
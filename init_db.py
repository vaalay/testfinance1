import sqlite3

DB = 'gestiune_clienti.db'

conn = sqlite3.connect(DB)
c = conn.cursor()

# -------------------- TABEL CLIENTI --------------------
c.execute('''
CREATE TABLE IF NOT EXISTS clienti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nume TEXT NOT NULL,
    prenume TEXT NOT NULL,
    email TEXT,
    telefon TEXT,
    adresa TEXT,
    data_nastere TEXT,
    stare_civila TEXT,
    cnp TEXT,
    serie_buletin TEXT,
    numar_buletin TEXT,
    eliberat_de TEXT,
    angajator TEXT,
    detalii_angajator TEXT,
    info_aditionale TEXT
)
''')

# -------------------- TABEL CREDITE --------------------
c.execute('''
CREATE TABLE IF NOT EXISTS credite (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_client INTEGER NOT NULL,
    suma REAL,
    dobanda REAL,
    com_adm REAL,
    dobanda_maj REAL,
    perioada INTEGER,
    data_inceput TEXT,
    data_sfarsit TEXT,
    status TEXT,
    FOREIGN KEY (id_client) REFERENCES clienti(id)
)
''')

# -------------------- TABEL CONTURI --------------------
c.execute('''
CREATE TABLE IF NOT EXISTS conturi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cod_cont TEXT NOT NULL,
    nume_cont TEXT NOT NULL,
    tip_cont TEXT,
    sold_debitor REAL,
    sold_creditor REAL,
    status_cont TEXT
)
''')

# -------------------- TABEL CONFIGURARE CREDITE --------------------
c.execute('''
CREATE TABLE IF NOT EXISTS config_credite (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tip_credit TEXT,
    dobanda REAL,
    com_adm REAL,
    com_dosar REAL,
    dobanda_maj REAL,
    perioada_luni INTEGER
)
''')

conn.commit()
conn.close()
print("Baza de date și tabelele au fost create cu succes!")

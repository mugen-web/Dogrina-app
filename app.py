from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'kutya123'
DATABASE = 'dogrina.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        conn.execute("""CREATE TABLE IF NOT EXISTS foglalas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kutya_nev TEXT,
            erkezes DATE,
            tavozas DATE,
            kennel INTEGER
        )""")
        conn.commit()
        conn.close()

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    foglalasok = conn.execute("SELECT * FROM foglalas").fetchall()
    conn.close()
    return render_template('index.html', foglalasok=foglalasok)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] in ['viktor', 'dorina'] and request.form['password'] == 'kutya123':
            session['user'] = request.form['username']
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/uj_foglalas', methods=['POST'])
def uj_foglalas():
    kutya_nev = request.form['kutya_nev']
    erkezes = request.form['erkezes']
    tavozas = request.form['tavozas']
    kennel = request.form['kennel']
    conn = get_db_connection()
    conn.execute("INSERT INTO foglalas (kutya_nev, erkezes, tavozas, kennel) VALUES (?, ?, ?, ?)",
                 (kutya_nev, erkezes, tavozas, kennel))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/torol/<int:id>')
def torol(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM foglalas WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

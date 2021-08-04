import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_institution(institution_id):
    conn = get_db_connection()
    institution = conn.execute('SELECT * FROM institution WHERE id = ?',
                        (institution_id,)).fetchone()
    conn.close()
    if institution is None:
        abort(404)
    return institution

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisalongsecretkeyfullofrand0mlettersabcgaefdasdf'

@app.route('/')

def index():

    conn = get_db_connection()
    institutions = conn.execute('SELECT i.ID, i.GroupID, i.Longname, i.Shortname, g.Name GroupName FROM Institution i INNER JOIN [Group] g ON ( i.GroupID = g.GroupID) ORDER BY i.Shortname ASC' ).fetchall()


    conn.close()
    return render_template('index.html', institutions=institutions)



@app.route('/institution/<int:institution_id>')
def institution(institution_id):
    institution = get_institution(institution_id)
    return render_template('institution.html', institution=institution)


@app.route('/institution/create', methods=('GET', 'POST'))
def create():
    return render_template('create.html')
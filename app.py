import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_single(table , column, id):
    conn = get_db_connection()
    institution = conn.execute('SELECT * FROM [{table}] WHERE {column} = {id}'.format(table=table , column=column, id=id)).fetchone()
    conn.close()
    if institution is None:
        abort(404)
    return institution

def get_all(table):
    conn = get_db_connection()
    groups = conn.execute('SELECT * FROM [{table}]'.format(table=table)).fetchall()
    conn.close()
    return groups

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisalongsecretkeyfullofrand0mlettersabcgaefdasdf'

@app.route('/')
def index():

    conn = get_db_connection()
    institutions = conn.execute('SELECT i.institutionID, i.GroupID, i.Longname, i.Shortname, g.Name GroupName FROM Institution i INNER JOIN [Group] g ON ( i.GroupID = g.GroupID) ORDER BY i.Shortname ASC' ).fetchall()
    conn.close()
    return render_template('index.html', institutions=institutions)



@app.route('/institution/<int:institution_id>')
def institution(institution_id):
    institution = get_single("institution", "institutionid", institution_id)
    return render_template('institution.html', institution=institution)


@app.route('/institution/create', methods=('GET', 'POST'))
def create():
    groups = get_all("Group")
    if request.method == 'POST':

        shortname = request.form['Longname']
        longname =  request.form['Shortname']
        groupid = request.form.get('group')
       
        if not shortname:
            flash('Shortname is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO Institution (GroupID, Shortname, Longname) VALUES (?, ?, ?)',
                         (groupid, shortname, longname))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))


    return render_template('create_institution.html', groups=groups)

@app.route('/institution/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    institution = get_single("institution", "institutionid", id)

    if request.method == 'POST':
        shortname = request.form['Longname']
        longname =  request.form['Shortname']
        groupid = request.form.get('group')

        if not longname:
            flash('longname is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE Institution SET groupid = ?, Longname = ? , Shortname = ?'
                         ' WHERE id = ?',
                         (groupid, longname, shortname, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit_institution.html', institution=institution)
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_single(table , column, id):
    conn = get_db_connection()
    institution = conn.execute('SELECT rowid, * FROM [{table}] WHERE {column} = {id}'.format(table=table , column=column, id=id)).fetchone()
    conn.close()
    if institution is None:
        abort(404)
    return institution

def get_all(table):
    conn = get_db_connection()
    groups = conn.execute('SELECT rowid, * FROM [{table}]'.format(table=table)).fetchall()
    conn.close()
    return groups

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisalongsecretkeyfullofrand0mlettersabcgaefdasdf'

@app.route('/')
def index():
    
    groups = get_all("Group")
    conn = get_db_connection()
    institutions = conn.execute('SELECT i.rowid, i.GroupID, i.Longname, i.Shortname, g.Name GroupName FROM Institution i INNER JOIN [Group] g ON ( i.GroupID = g.rowid) ORDER BY i.Shortname ASC' ).fetchall()
    institutions = conn.execute('SELECT i.InstitutionID, i.GroupID, i.Longname, i.Shortname, p.PreferenceID, p.Universities, p.Years, p.WTE, p.SuggestedAllocation, p.AgreedAllocation, p.Year, p.Capacity, g.Name FROM Institution i INNER JOIN Preference p ON ( i.InstitutionID = p.InstitutionID  ) INNER JOIN [Group] g ON ( i.GroupID = g.GroupID ) ').fetchall()
    conn.close()
    return render_template('index.html', institutions=institutions, groups=groups)



@app.route('/institution/<int:institution_id>')
def institution(institution_id):
    institution = get_single("institution", "rowid", institution_id)
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
    institution = get_single("institution", "rowid", id)
    groups = get_all("Group")
    
    if request.method == 'POST':
        longname = request.form['Longname']
        shortname =  request.form['Shortname']
        groupid = request.form.get('group')

        if not longname:
            flash('longname is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE Institution SET groupid = ?, Longname = ? , Shortname = ?'
                         ' WHERE rowid = ?',
                         (groupid, longname, shortname, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit_institution.html', institution=institution, groups = groups)


    #ajax calls

@app.route('/_update_index')
def add_numbers():
    field = request.args.get('field', 0, type=str)
    id = request.args.get('id', 0, type=str)
    value = request.args.get('value', 0, type=str)

    conn = get_db_connection()
    conn.execute('UPDATE Institution SET '+field+' = ?'
                'WHERE InstitutionID = ?',
                (value, id))
    conn.commit()
    conn.close()

    return jsonify(result=field + id + value)
#currently moving through https://towardsdatascience.com/sending-data-from-a-flask-app-to-postgresql-database-889304964bf2

import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from werkzeug.exceptions import abort
from models import db, Institution, Group, Preference


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisalongsecretkeyfullofrand0mlettersabcgaefdasdf'
app.config["SQLALCHEMY_ECHO"] = True

# our database uri
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://orthoptic:gladdylight@localhost:5432/orthopticequitable"



db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    
    groups=Group.query.all()
    #institutions = db.session.query(Institution, Preference).join(Preference, Preference.institutionid == Institution.id).all()
    results = db.session.query(Institution, Preference).join(Preference, Preference.institutionid == Institution.id, isouter=True).all()

    return render_template('index.html', results=results, groups=groups)



@app.route('/institution/<int:institution_id>')
def institution(institution_id):

    institution=Institution.query.get(institution_id)

    return render_template('institution.html', institution=institution)


@app.route('/institution/create', methods=('GET', 'POST'))
def create():
    
    groups=Group.query.all()
 
     
    if request.method == 'POST':
        shortname = request.form['Longname']
        longname =  request.form['Shortname']
        groupid = request.form.get('group')


        print ("incoming request id")
        print(request.form.get('group'))
       
        if not shortname:
            flash('Shortname is required!')
        else:
            entry = Institution(groupid, longname, shortname)
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('index'))

    #postgres_create
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
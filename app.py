#currently moving through https://towardsdatascience.com/sending-data-from-a-flask-app-to-postgresql-database-889304964bf2

import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from werkzeug.exceptions import abort
from models import db, Institution, Group, Preference, University, Placement


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
    
    prefs = {}
    prefs['selected'] = "index"

    groups=Group.query.all()
    #institutions = db.session.query(Institution, Preference).join(Preference, Preference.institutionid == Institution.id).all()
    results = db.session.query(Institution, Preference).join(Preference, Preference.institutionid == Institution.id, isouter=True).order_by("shortname").all()

    return render_template('index.html', results=results, groups=groups, prefs=prefs)


@app.route('/university')
def university():
    
    prefs = {}
    prefs['selected'] = "university"
    universities=University.query.all()

    return render_template('index.html', universities=universities, prefs=prefs)


@app.route('/institution')
def institution_index():

    prefs = {}
    prefs['selected'] = "insitution"

    groups=Group.query.all()
    #institutions = db.session.query(Institution, Preference).join(Preference, Preference.institutionid == Institution.id).all()
    results = db.session.query(Institution, Preference).join(Preference, Preference.institutionid == Institution.id, isouter=True).order_by("shortname").all()

    return render_template('institution_index.html', results=results, groups=groups, prefs=prefs )


@app.route('/institution/<int:institution_id>')
def institution(institution_id):

    prefs = {}
    prefs['selected'] = "index"

    institution=Institution.query.get(institution_id)

    return render_template('institution.html', institution=institution, prefs=prefs )


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
    institution=Institution.query.get(id)
    groups=Group.query.all()
    
    if request.method == 'POST':
        institution.longname = request.form['Longname']
        institution.shortname =  request.form['Shortname']
        institution.groupid = request.form.get('group')

        if not request.form['Longname']:
            flash('longname is required!')
        else:
            db.session.commit()
            return redirect(url_for('index'))
            

    return render_template('edit_institution.html', institution=institution, groups = groups)


    #ajax calls

@app.route('/_update_index')
def add_numbers():
    field = request.args.get('field', 0, type=int)
    id = request.args.get('id', 0, type=str)
    value = request.args.get('value', 0, type=str)

    if field == "longname" or field == "shortname":
        institution=Institution.query.get(id)
        setattr(institution,field,value)
        db.session.commit()
    else:
        if not id:
            #insert new preference
            entry = Preference(None,None,None,None,None,None,None,None,None)
            db.session.add(entry)
            db.session.commit()

            #added a blank preference, now update it with the result
            #refreshing is not a good way to do it..

            #now you need to refresh the page

            return jsonify(result="refresh")

        else:
            preference=Preference.query.get(id)
            setattr(preference,field,value)
            db.session.commit()

    return jsonify(result=field + id + value)


@app.route('/report')
def report():
    prefs = {}
    prefs['selected'] = "report"

 

    return render_template('dashboard.html', prefs=prefs )
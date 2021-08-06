from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Institution(db.Model):
    __tablename__ = 'institution'
    id = db.Column(db.Integer, primary_key=True)
    groupid = db.Column(db.Integer, db.ForeignKey('group.id') )
    longname = db.Column(db.String(255))
    shortname = db.Column(db.String(255))

    def __init__(self, groupid, longname, shortname):
        self.groupid = groupid
        self.longname = longname
        self.shortname = shortname

class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

class Preference(db.Model):
    __tablename__ = 'preference'
    id = db.Column(db.Integer, primary_key=True)
    institutionid = db.Column(db.Integer, db.ForeignKey('institution.id'))
    universities = db.Column(db.String(255))
    years = db.Column(db.String(255))
    capacity = db.Column(db.Integer)
    wte = db.Column(db.Float)
    suggestedallocation = db.Column(db.Integer)
    agreedallocation = db.Column(db.Integer)
    year = db.Column(db.Integer)
    institutions = db.relationship(Institution, backref='topic')

    def __init__(self, name, institutionid, universities, years, capacity, wte, suggestedallocation, agreedallocation, year):
        self.name = name
        self.institutionid = institutionid
        self.universities = universities
        self.years = years
        self.capacity = capacity
        self.wte = wte
        self.suggestedallocation = suggestedallocation
        self.agreedallocation = agreedallocation
        self.year = year


class Placement(db.Model):
    __tablename__ = 'placement'
    id = db.Column(db.Integer, primary_key=True)
    universityid = db.Column(db.Integer, db.ForeignKey('university.id'))
    institutionid = db.Column(db.Integer, db.ForeignKey('institution.id'))
    year = db.Column(db.String(255))
    date = db.Column(db.Date)

    def __init__(self, universityid, preferenceid, year, date):
        self.universityid = universityid
        self.preferenceid = preferenceid
        self.year = year
        self.date = date


class University(db.Model):
    __tablename__ = 'university'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


    def __init__(self, name):
        self.name = name


from ourapp import app, db, User
app.app_context().push()
db.create_all()
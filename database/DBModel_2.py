# from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
# engine = create_engine('sqlite:///college.db', echo = True)
# meta = MetaData()
#
# students = Table(
#    'students', meta,
#    Column('id', Integer, primary_key = True),
#    Column('name', String),
#    Column('lastname', String),
# )
#
#
# User = Table(
#     'user', meta,
#     Column('id', Integer, primary_key=True),
#     Column('username', String(64), index=True, unique=True),
#     Column('email', String(120), index=True, unique=True),
#     Column('password_hash', String(128))
# )
#
#
# meta.create_all(engine)



from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/QA.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    email_2 = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class MyUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    def __repr__(self):
        return '<User %r>' % self.username
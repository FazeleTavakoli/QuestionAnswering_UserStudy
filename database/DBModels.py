from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# from app import db
# from app import login
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String


Base = declarative_base()
# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))

engine = create_engine('sqlite:////Users/fazeletavakoli/PycharmProjects/QA_userStrudy/database/QA2.db')
create_tables = True

class User(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password = Column(String(128))
    # answeredQuestions = db.relationship('AnsweredQuestion', backref='participant', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


#     def __repr__(self):
#         return '<User {}>'.format(self.username)
#
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
#
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
#
#
class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    question = Column(String(128))
    # answer = Column(String(64))   //I omitted this entry from Question table in DB, for now
    sparqlQuery = Column(String(300))
    controlledLanguage = Column(String(128))   #sparqltoUser
    # answeredQuestions = relationship('AnsweredQuestion', backref='askedQuestion', lazy='dynamic')

    def __init__(self, question, sparqlQuery, controlledLanguage):
        self.question = question
        # self.answer = answer
        self.sparqlQuery = sparqlQuery
        self.controlledLanguage = controlledLanguage

# class AnsweredQuestion(Base):
#     __tablename__ = "answeredQuestions"
#     user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
#     questionId = Column(Integer, ForeignKey('question.id'), primary_key=True)
#     timestamp = Column(DateTime, default=datetime.utcnow)
#     duration = Column(Integer)
#     answered = Column(String(16))
#     logRecord = Column(String(32))
#     def __init__(self, ):

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key= true)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=false)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=false)
    user_answer = Column(String(128))
    skipped = Column(Boolean)
    skipped_reason = Column(String(128))
    time = Column(DateTime)
    def __init__(self,user_id, question_id, user_answer, skipped, skipped_reason, time):
        self.user_id = user_id
        self.question_id = question_id
        self.user_answer = user_answer
        self.skipped = skipped
        self.skipped_reason = skipped_reason
        self.time = time

# db.metadata.clear()
# db.metadata.reflect(engine=engine)
#db.create_all()

if create_tables:
    # db.Model.metadata.create_all(engine)
    Base.metadata.create_all(engine)

# if __name__ == '__main__':
#     # db.metadata.clear()
#     # meta = MetaData()
#     # engine = create_engine('sqlite:///database/QA.db')
#     # Base.metadata.create_all(engine)
#     # meta.create_all(engine)
#     # create_tables = True
#     if create_tables:
#         db.Model.metadata.create_all(engine)
#     # db.create_all()
#     u = User(username='john', email='john@example.com', password = "123123123")
#     db.session.add(u)
#     db.session.commit()
#     a = 8
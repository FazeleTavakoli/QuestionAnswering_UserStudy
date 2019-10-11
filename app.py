import flask
from forms.loginForm import LoginForm
from forms.registerForm import RegisterForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, flash, render_template, redirect, url_for, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from database.DBModels import User, Question, Interaction
import json
import urllib.request
import urllib.parse
import requests
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/fazeletavakoli/Downloads/QA_userStrudy/QA_userStrudy/database/QA.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/fazeletavakoli/PycharmProjects/QA_userStrudy/database/QA2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login = LoginManager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
#migrate = Migrate(app, db)
# from database.DBModels import User, Question, AnsweredQuestion

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))

@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))
        flash('Error: Invalid username or password')

    return render_template('login.html', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('New user has been created!')
    # readJsonFile()
    # question = db.session.query(Question).get(1)
    # question = db.session.query(Question).all()
    # a = 1

    return render_template('signup.html', form=form)

# @app.route('/survey')
# @login_required
# def survey():
#     for i in range(2):
#         readJsonFile()
#         # data = {'userid': current_user.username}
#         question = db.session.query(Question).all()
#         # data['question'] = question
#         q = 1
#         q = question[1].answer
#         return render_template('survey.html', title='Survey', user=current_user, question=question[i],
#                                user_id=current_user.id)
#
#     # return render_template('survey.html', title='Survey', user = current_user, question = question, user_id = current_user.id)

@app.route('/d3_Visualization')
def d3_Visualization(sparql_query = ''):
    # sparql_query = sparql_query
    return render_template('d3_Visualization.html', sparql_query=sparql_query)

@app.route('/survey/<key>')
@login_required
def survey(key):
    data = {'userid': current_user.username}
    questions = db.session.query(Question).all()
    return render_template('survey.html', questions = questions, key = key, user=current_user)


@app.route('/question/<key>')
def question(key):
    readJsonFile()
    questions = db.session.query(Question).all()
    # single_question = questions.get(key)
    single_question = questions[int(key)]
    # question_id =
    session['question_id'] = single_question.id
    if not single_question:
        abort(404)
    key = int(key) + 1
    fileName = "kg_" + str(key) + ".png"
    imageFile = url_for('static', filename = fileName)
    a = single_question.sparqlQuery
    d3_Visualization(sparql_query = a)
    return render_template('question.html', single_question = single_question, key = key, user=current_user, imageFile = imageFile)

@app.route('/correct/<key>')
@login_required
def correct(key):
    save_user_answers(user_answer='yes')

    return redirect(url_for('question', key = key))

@app.route('/wrong/<key>')
@login_required
def wrong(key):
    save_user_answers(user_answer='no')
    return redirect(url_for('question', key=key))

@app.route('/skip/<key>')
def skip(key):
    reason = 'skip'
    if 'reason' in flask.request.values:
        reason = flask.request.values['reason']
    save_user_answers(skipped=True, skipped_reason= reason)
    return redirect(url_for('question', key=key))

def save_user_answers(user_answer='', skipped = False, skipped_reason = ''):
    time = datetime.datetime.utcnow()
    record = Interaction(current_user.id, session['question_id'], user_answer, skipped, skipped_reason, time)
    db.session.add(record)
    db.session.commit()

# @app.route('/save_answers')
# @login_required
# def save_answers():
#     save_user_answers(data)
#     return redirect()


# def log_interaction(interaction='', answer='', data=''):
#     log_record = InteractionLog(current_user.username,
#                                 session['question_id'],
#                                 session['session_id'],
#                                 interaction,
#                                 answer,
#                                 session['current_query'],
#                                 datetime.datetime.utcnow(),
#                                 data)
#     db.session.add(log_record)
#     db.session.commit()

def readFile(address):
    qusetionList = []
    with open(address) as f:
        for line in f:
           if line:
                qusetionList.append(line)
    return qusetionList

#producing questions table in database
def readJsonFile():
    questionCounter = 0
    address_lcquad_1 = "/Users/fazeletavakoli/PycharmProjects/QA_userStrudy/LC-QuAD-train.json"
    address_lcquad_2 = "/Users/fazeletavakoli/PycharmProjects/QA_userStrudy/lcquad_2_0.json"
    questionList = readFile("/Users/fazeletavakoli/PycharmProjects/QA_userStrudy/sparqlToUser.txt")
    answerList = readFile("/Users/fazeletavakoli/PycharmProjects/QA_userStrudy/answers.txt")

    with open(address_lcquad_1, 'r') as jsonFile:
        dictionary = json.load(jsonFile)
    for entity in dictionary:
         if questionCounter != 3:
            questionId = questionCounter
            # question = entity['paraphrased_question']
            question = entity['corrected_question']
            # answer = answerList[questionCounter]
            # query = entity["sparql_dbpedia18"]
            query = entity["sparql_query"]
            ### using 'SparqltoUser' webservice for getting interpretation of sparql query ###
            # query = "SELECT DISTINCT ?x WHERE {<http://www.wikidata.org/entity/Q20034> <http://www.wikidata.org/prop/direct/P527> ?x . } limit 1000"
            language = "en"
            # knowledgeBase = "wikidata"  # it doesn't work with "wikidata" when api is used not my local host.
            knowledgeBase = "dbpedia"
            # response = requests.get('https://qanswer-sparqltouser.univ-st-etienne.fr/sparqltouser',
            #                         params={'sparql':query, 'lang':language,'kb':knowledgeBase})  # this command also works without setting 'lang' and 'kb'
            response = requests.get('http://localhost:1920/sparqltouser',
                                    params={'sparql': query, 'lang': language, 'kb': knowledgeBase})
            jsonResponse = response.json()
            controlledLanguage = jsonResponse['interpretation']
            # controlledLanguage = questionList[questionCounter]
            questionCounter = questionCounter + 1
            new_question = Question(question = question, sparqlQuery= query, controlledLanguage= controlledLanguage)  # the argument "answer = answer" has been omitted
            db.session.add(new_question)
            db.session.commit()
            # d3_Visualization(query)





if __name__ == '__main__':
    # readJsonFile()
    app.run()

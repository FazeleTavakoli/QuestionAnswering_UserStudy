from flask_wtf import Form
from wtforms import TextField, BooleanField, SelectMultipleField, widgets, RadioField, SelectField


class AssessmentForm(Form):
    # question_1 = RadioField('The whole structure of the survey was easy to follow:',
    #                      choices=[('yes','Yes'),('no','No')])
    #
    # question_2 = RadioField('It was easy to understand the relationship between different parts of every question:',
    #                         choices=[('yes', 'Yes'), ('no', 'No')])

    question_1 = SelectField('The whole structure of the survey was easy to follow:',
                                     choices= [('Empty', ''),('5','5'), ('4','4'), ('3', '3'), ('2', '2'), ('1', '1')])


    question_2 = SelectField('It was easy to understand the relationship between different parts of every question:',
                             choices=[('Empty', ''), ('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1')])
from flask import Flask, render_template, session, redirect, url_for, flash
from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, SelectField, DateTimeField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Optional
from wtforms import ValidationError
from wtforms.validators import Regexp




# class RegistrationForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(),Email()])
#     gebruikersnaam = StringField('Gebruikersnaam', validators=[DataRequired()])
#     wachtwoord = PasswordField('Wachtwoord', validators=[DataRequired()])
#     submit = SubmitField('Registeren')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Gebruikersnaam', validators=[DataRequired()])
    woonplaats = StringField('Woonplaats', validators=[DataRequired()])
    huisnummer = StringField('Huisnummer', validators=[DataRequired()])
    toevoeging = StringField('toevoeging')
    straat = StringField('Straat', validators=[DataRequired()])
    postcode = StringField('Postcode', validators=[DataRequired(), Regexp('^\d{4}[A-Za-z]{2}$', message='Ongeldige postcode!')])
    password = PasswordField('Wachtwoord', validators=[DataRequired(), EqualTo('pass_confirm', message='Wachtwoorden moeten gelijk zijn!')])
    pass_confirm = PasswordField('Bevestig uw wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Registeren!')

    def validate_woonplaats(self, field):
        if not field.data.replace('.', '').replace('-', '').isalpha():
            raise ValidationError('ongeldige woonplaats')

    def validate_straat(self, field):
        if not field.data.replace('.', '').replace('-', '').isalpha():
            raise ValidationError('ongeldige straatnaam.')
    
    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Dit e-mailadres staat al geregistreerd!')
    
    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Deze gebruikersnaam is al in gebruik, probeer een ander naam!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Inloggen')



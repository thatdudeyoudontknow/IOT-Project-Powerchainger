from flask import Flask, render_template, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,EmailField, HiddenField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email
from wtforms import ValidationError


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    gebruikersnaam = StringField('Gebruikersnaam', validators=[DataRequired()])
    wachtwoord = PasswordField('Wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Registeren')


class LoginForm(FlaskForm):
    gebruikersnaam = StringField('Gebruikersnaam', validators=[DataRequired()])
    wachtwoord = PasswordField('wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Inloggen')


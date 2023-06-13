from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField #, HiddenField, SelectField, DateTimeField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError


class RegistrationForm(FlaskForm):
    email = StringField('', validators=[DataRequired(),Email()])
    username = StringField('', validators=[DataRequired()])
    password = PasswordField('', validators=[DataRequired(), EqualTo('',    message='')])
    pass_confirm = PasswordField('', validators=[DataRequired()])
    submit = SubmitField('')
    
    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('')
    
    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('')
        





        
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Inloggen')
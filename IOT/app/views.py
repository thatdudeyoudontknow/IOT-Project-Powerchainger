from app import app
from flask import render_template
from flask_login import LoginManager
from app.forms import LoginForm

@app.route("/")
def homepage():
    return render_template("public/login.html")


@app.route("/home")
def test1():
    return render_template("public/home.html")

@app.route("/competitie")
def test():
    return render_template("public/competitie.html")

@app.route("/graphwb")
def graph():
    return render_template("public/graphwb.html")

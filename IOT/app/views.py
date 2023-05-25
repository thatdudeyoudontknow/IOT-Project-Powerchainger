from app import app
from flask import render_template


@app.route("/login")
def login():
    return render_template("public/login.html")


@app.route("/home")
def home():
    return render_template("public/home.html")

@app.route("/competitie")
def competitie():
    return render_template("public/competitie.html")

@app.route("/bezuinigen")
def bezuinigen():
    return render_template("public/bezuinigen.html")
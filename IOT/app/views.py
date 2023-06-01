from app import app
from flask import render_template
from flask_login import LoginManager


@app.route("/")
def home():
    return render_template("public/home.html")

@app.route("/competitie")
def competitie():
    return render_template("public/competitie.html")

@app.route("/bezuinigen")
def bezuinigen():
    return render_template("public/bezuinigen.html")

@app.route("/graph")
def graph():
    return render_template("public/graph.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        if not url_has_allowed_host_and_scheme(next, request.host):
            return flask.abort(400)
        return flask.redirect(next or flask.url_for('index'))
    return render_template("public/login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/home")
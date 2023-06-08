from app import app
from flask import Flask, jsonify, render_template
from flask_login import LoginManager
import sqlite3
from flask_cors import CORS
import datetime



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

@app.route("/data")
def get_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('mqtt_messages.db')
    cursor = conn.cursor()

    # Execute a query to retrieve data from the database
    query = "SELECT timestamp, message FROM mqtt_messages"
    cursor.execute(query)

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Close the database connection
    conn.close()

    results = []

    # Process the rows and add 2 hours to the timestamp
    for row in rows:
        timestamp = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
        adjusted_timestamp = (timestamp + datetime.timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
        results.append({'timestamp': adjusted_timestamp, 'message': row[1]})

    return jsonify(results)



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
# @login_required
def logout():
    logout_user()
    return redirect("/home")
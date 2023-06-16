from app import app
from flask import Flask, jsonify, render_template
from flask_login import LoginManager
import sqlite3
from flask_cors import CORS
import datetime
import os
# from app import 
# from app.forms import LoginForm

db = 'data.sqlite'

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

@app.route("/login", methods=["GET", "POST"])
def login2():
    return render_template("public/login2.html")

@app.route("/huidige_woning")
def get_huidige_woning():
    userID = 2
    # Connect to the SQLite database
    database_path = os.path.join(os.path.dirname(__file__), 'data.sqlite')

    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Execute a query to retrieve data from the database
    query = "SELECT huisnaam FROM huis WHERE huisID IN (SELECT huisID FROM HKU WHERE userID = ?)"
    cursor.execute(query, (userID,))  # Pass the userID as a parameter
    
    # Fetch all the results
    results = cursor.fetchall()

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    # Process the results as needed
    # ...

    return "Data retrieved successfully"



# data dat word uit de database gehaald voor de grafiek
@app.route("/data")
def get_data():
    userID = 1
    # Connect to the SQLite database
    database_path = os.path.join(os.path.dirname(__file__), 'data.sqlite')

    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Execute a query to retrieve data from the database
    query = "SELECT datetime, verbruik FROM verbruik WHERE huisID IN (SELECT huisID FROM HKU WHERE userID = ?)"
    cursor.execute(query, (userID,))  # Pass the userID as a parameter

    # Fetch all rows from the cursor
    rows = cursor.fetchall()

    # Close the database connection
    conn.close()

    results = []

    # Process the rows without modifying the timestamp
    for row in rows:
        timestamp = row[0]
        message = row[1]
        results.append({'timestamp': timestamp, 'message': message})

    return jsonify(results)


# data word uit de database gehaald om de laatste waardes op te halen voor het huidig verbruik
@app.route('/huidig_verbruik')
def get_current():
    # Get the absolute path of the database file in the current directory
    database_path = os.path.join(os.path.dirname(__file__), 'data.sqlite')

    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Execute a query to retrieve the latest numerical value from the database
    query = "SELECT message FROM mqtt_messages ORDER BY timestamp DESC LIMIT 1"
    cursor.execute(query)

    # Fetch the latest message
    row = cursor.fetchone()

    # Close the database connection
    conn.close()

    if row is None:
        # No messages found in the database
        return jsonify({'error': 'No messages found.'})

    # Extract the numerical value from the message
    numerical_value = float(row[0])

    return jsonify({'value': numerical_value})


if __name__ == '__main__':
    app.run()





# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():

#         login_user(user)

#         flask.flash('Logged in successfully.')

#         next = flask.request.args.get('next')
#         if not url_has_allowed_host_and_scheme(next, request.host):
#             return flask.abort(400)
#         return flask.redirect(next or flask.url_for('index'))
#     return render_template("public/login.html", form=form)



@app.route("/logout")
# @login_required
def logout():
    logout_user()
    return redirect("/home")
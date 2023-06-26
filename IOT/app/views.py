from app import app
from flask import Flask, jsonify, render_template, request
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

@app.route("/vrienden")
def vrienden():
    return render_template("public/vrienden.html")

@app.route("/login", methods=["GET", "POST"])
def login2():
    return render_template("public/login2.html")


@app.route("/huidige_woning")
def get_current_huisnaam():
    userID = 1  # Replace with the actual current user ID

    # Connect to the SQLite database
    database_path = os.path.join(os.path.dirname(__file__), 'data.sqlite')
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Execute a query to retrieve the current huisnaam from the current user
    query = "SELECT huisnaam FROM huis WHERE huisID IN (SELECT huisID FROM HKU WHERE userID = ?)"
    cursor.execute(query, (userID,))

    # Fetch the result
    result = cursor.fetchone()

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    if result is not None:
        huisnaam = result[0]
        return jsonify({'value': huisnaam})  # Return JSON response
    else:
        return jsonify({'error': 'No current huisnaam found for the user'})  # Return JSON response



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
        results.append({'datetime': timestamp, 'verbruik': message})

    return jsonify(results)


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


# -----------------------------------------------------------------------------------
# het zoeken van vrienden

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form['search_query']

    # Get the absolute path of the database file in the current directory
    database_path = os.path.join(os.path.dirname(__file__), 'data.sqlite')

    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Execute the search query
    cursor.execute("SELECT gebruikersnaam FROM user WHERE gebruikersnaam LIKE ?", ('%' + search_query + '%',))
    results = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    return render_template('public/zoek_vrienden.html', results=results)

if __name__ == '__main__':
    app.run()



# -----------------------------------------------------------------------------------
# de verbruik per dag van vrienden laten zien

@app.route('/vrienden_verbruik_per_dag')
def get_total_vrienden():
    userIDs = [1, 2]  # List of userIDs
    total_verbruik_per_user = {}

    # Get the absolute path of the database file in the current directory
    database_path = os.path.join(os.path.dirname(__file__), 'data.sqlite')

    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Execute a query to retrieve the sum of verbruik values for each user and the current day
    query = """
        SELECT user.gebruikersnaam, SUM(verbruik.verbruik)
        FROM verbruik
        JOIN user ON verbruik.userID = user.userID
        WHERE verbruik.huisID IN (SELECT huisID FROM HKU WHERE userID IN ({user_ids_placeholder}))
            AND DATE(verbruik.datetime) = DATE('now', 'localtime')
        GROUP BY verbruik.userID
    """.format(user_ids_placeholder=','.join('?' for _ in userIDs))

    cursor.execute(query, userIDs)  # Pass the userIDs as parameters

# Fetch the rows containing the sum of verbruik values per user along with usernames
    rows = cursor.fetchall()

# Iterate over the rows and store the verbruik per user with usernames
    for row in rows:
        username = row[0]
        total_verbruik = float(row[1])
        total_verbruik_per_user[username] = total_verbruik

# Close the database connection
    conn.close()

    if total_verbruik_per_user:
        return jsonify(total_verbruik_per_user)
    else:
        return "No data found for the current day."

    
# -----------------------------------------------------------------------------------
# verbruik per dag van de huidige gebruiker
@app.route('/huidig_verbruik')
def get_current():
    userID = 1
    # Get the absolute path of the database file in the current directory
    database_path = os.path.join(os.path.dirname(__file__), 'data.sqlite')

    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Execute a query to retrieve the latest numerical value from the database
    query = "SELECT verbruik FROM verbruik WHERE huisID IN (SELECT huisID FROM HKU WHERE userID = ?) ORDER BY datetime DESC LIMIT 1"
    cursor.execute(query, (userID,))  # Pass the userID as a parameter

    # Fetch the latest message
    row = cursor.fetchone()

    # Close the database connection
    conn.close()

    if row is None:
        # No messages found in the database
        return jsonify({'error': 'geen gebruik gevonden'})

    # Extract the numerical value from the message
    numerical_value = float(row[0])

    return jsonify({'value': numerical_value})

# from app.forms import RegistrationForm
import os
from app import app
from flask import Flask, jsonify, render_template, request,redirect, request, url_for, flash, abort
from flask_login import LoginManager,login_user, login_required, logout_user, current_user 
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash
from functools import wraps
import sqlite3
import datetime
import json


app.config['SECRET_KEY'] = 'X11gc3N5hb78RGyKY4qk5qHZ8aqC4Ch7'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

db = SQLAlchemy(app)


from app.models import User , Kamer, Huis, HKU
from app.forms import RegistrationForm, LoginForm, HuisForm, KamerForm


@app.route("/")
def home():
    return render_template("public/home.html", name=current_user)

@app.route("/competitie")
def competitie():
    return render_template("public/competitie.html", name=current_user)

@app.route("/bezuinigen")
def bezuinigen():
    return render_template("public/bezuinigen.html", name=current_user)

@app.route("/graph")
def graph():
    return render_template("public/graph.html", name=current_user)

@app.route("/vrienden")
def vrienden():
    return render_template("public/vrienden.html", name=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'Je bent nu uitgelogd!', 'success')
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_email = User.query.filter_by(email=form.email.data).first()
        user_username = User.query.filter_by(username=form.username.data).first()

        if user_email:
            flash(u'Dit emailadres is al in gebruik. Kies een ander emailadres.', 'warning')
        elif user_username:
            flash(u'Deze gebruikersnaam is al in gebruik. Kies een andere gebruikersnaam.', 'warning')

        else:
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data,
                        )

            db.session.add(user)
            db.session.commit()



            flash(u'Dank voor de registratie. Er kan nu ingelogd worden! ', 'success')
            return redirect(url_for('login'))
    elif form.email.errors:
        flash(u'Dit email is incorrect')    

    elif form.password.errors:
        flash(u'Wachtwoord komt niet overeen')

    return render_template('public/registreren.html', form=form)



@app.route('/huisconfig', methods=['GET', 'POST'])
def huisconfig():
    form = HuisForm()
    kamer_form = KamerForm()

    if form.validate_on_submit() and kamer_form.validate_on_submit():
        # Create a new huis instance
        huis = Huis(
            woonplaats=form.woonplaats.data,
            huisnummer=form.huisnummer.data,
            toevoeging=form.toevoeging.data,
            straat=form.straat.data,
            postcode=form.postcode.data
        )

        # Create a new kamer instance
        kamer = Kamer(
            huisnummer=kamer_form.huisnummer.data,
            kamernaam=kamer_form.kamernaam.data
        )

        # Add the huis and kamer to the database
        db.session.add(huis)
        db.session.add(kamer)
        db.session.commit()

        # Call the insert_hku() function to insert the huisID and kamerID into the HKU table
        insert_hku(current_user.id, huis.huisID, kamer.kamerID)

        flash('de registratie is gelukt', 'success')

    return render_template('public/huisconfig.html', form=form, kamer_form=kamer_form, name=current_user)

def insert_hku(user_id, huis_huisID, kamer_kamerID):
    database_path = os.path.join(os.path.dirname(__file__), 'data.sqlite')
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Insert the values into the 'HKU' table
    cursor.execute('INSERT INTO HKU (huisID, kamerID, userID) VALUES (?, ?, ?)',
                   (huis_huisID, kamer_kamerID, user_id))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash(u'Succesvol ingelogd.', 'success')
    
            next = request.args.get('next')
            if not next or url_parse(next).netloc != '':
                next = url_for('home')
            return redirect(url_parse(next).path)
        
        else:
            print(u'U email of wachtwoord is niet correct.', 'warning')     
    elif form.email.errors:  
        print(u'u email is niet bestaand', 'warning')
    return render_template('public/login2.html', form=form) 


    

@app.route("/huidige_woning")
def get_current_huisnaam():
    userID = current_user.id # Replace with the actual current user ID

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
    userID = current_user.id
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
    cursor.execute("SELECT username, id FROM user WHERE username LIKE ?", ('%' + search_query + '%',))
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
        SELECT user.username, SUM(verbruik.verbruik)
        FROM verbruik
        JOIN user ON verbruik.userID = user.id
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
# huidig verbruik van de huidige gebruiker
@app.route('/huidig_verbruik')
def get_current():
    userID = current_user.id
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
        return jsonify({'error': 'geen verbruik gevonden'})

    # Extract the numerical value from the message
    numerical_value = float(row[0])

    return jsonify({'value': numerical_value})


# -----------------------------------------------------------------------------------
# verbruik per dag van de huidige gebruiker
@app.route('/verbruik_per_dag')
def dagverbruik():
    userID = current_user.id

    # Get the absolute path of the database file in the current directory
    database_path = os.path.join(os.path.dirname(__file__), 'data.sqlite')

    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Execute a query to retrieve the sum of verbruik values for the user and the current day
    query = """
        SELECT user.username, SUM(verbruik.verbruik)
        FROM verbruik
        JOIN user ON verbruik.userID = user.id
        WHERE verbruik.huisID IN (SELECT huisID FROM HKU WHERE userID = ?)
            AND DATE(verbruik.datetime) = DATE('now', 'localtime')
        GROUP BY verbruik.userID
    """

    cursor.execute(query, (userID,))  # Pass the user ID as a parameter

    # Fetch the rows containing the sum of verbruik values per user along with usernames
    # Fetch the latest message
    row = cursor.fetchone()

    # Close the database connection
    conn.close()

    if row is None:
        # No messages found in the database
        return jsonify({'error': 'geen verbruik gevonden'})

    # Extract the numerical value from the message
    numerical_value = float(row[1])

    return jsonify({'value': numerical_value})

# -----------------------------------------------------------------------------------
# verzend de vrienden ID's naar de database

@app.route('/process_users', methods=['POST'])
def process_users():
    userID = 1 
    selected_user_ids = request.form.getlist('userID')
    
    # Connect to the SQLite database
    database_path = os.path.join(os.path.dirname(__file__), 'data.sqlite')
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Create the "verzoeken" table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS verzoeken (
        verzoekID INTEGER PRIMARY KEY AUTOINCREMENT,
        userID INTEGER NOT NULL,
        vriendenID INTEGER NOT NULL,
        status TEXT,
        FOREIGN KEY(userID) REFERENCES user(userID),
        FOREIGN KEY(vriendenID) REFERENCES user(userID)
    )''')

    # Insert invitation records for selected users
    for user_id in selected_user_ids:
        cursor.execute("INSERT INTO verzoeken (userID, vriendenID, status) VALUES (?, ?, ?)",
                       (userID, user_id, "pending"))

    # Commit the changes and close the database connection
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Invitations sent successfully", "success")

    return redirect(url_for('competitie'))


# -----------------------------------------------------------------------------------
# zorg dat de vriendverzoek ontvangen word en geacepteerd of afgeslagen kan worden


@app.route('/accept_decline_invitation/<int:invitation_id>', methods=['GET', 'POST'])
def accept_decline_invitation(invitation_id):
    # Connect to the SQLite database
    database_path = os.path.join(os.path.dirname(__file__), 'data.sqlite')
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Retrieve the invitation details from the "verzoeken" table
    cursor.execute("SELECT userID, vriendenID, status FROM verzoeken WHERE verzoekID = ?", (invitation_id,))
    invitation = cursor.fetchone()

    # Check if the invitation exists
    if invitation is None:
        return "Invitation not found"

    inviter_id, invitee_id, status = invitation

    if request.method == 'GET':
        return render_template('verzoek.html', inviter_id=inviter_id, invitee_id=invitee_id)

    elif request.method == 'POST':
        # Retrieve the user's response (accept or decline) from the form
        response = request.form.get('response')

        # Update the invitation status in the database based on the response
        if response == 'accept':
            new_status = 'accepted'
        elif response == 'decline':
            new_status = 'declined'
        else:
            return "Invalid response"

        cursor.execute("UPDATE verzoeken SET status = ? WHERE verzoekID = ?", (new_status, invitation_id))
        conn.commit()

        cursor.close()
        conn.close()

        return "Invitation response recorded"

    cursor.close()
    conn.close()

# -----------------------------------------------------------------------------------
# zorg dat de kamerID en huisID in hku word gezet

@app.route('/insert_hku', methods=['POST'])
def insert_hku():
        # Connect to the SQLite database
    database_path = os.path.join(os.path.dirname(__file__), 'data.sqlite')
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Get the current user ID from the request (you may need to modify this depending on your authentication setup)
    current_user_id = request.form.get('current_user_id')

    # Query the 'huis' table to get the huisID based on the userID
    cursor.execute('SELECT huisID FROM huis WHERE userID = ?', (current_user_id,))
    huis_id = cursor.fetchone()[0]

    # Query the 'kamer' table to get the kamerID based on the userID
    cursor.execute('SELECT kamerID FROM kamer WHERE userID = ?', (current_user_id,))
    kamer_id = cursor.fetchone()[0]

    # Insert the values into the 'HKU' table
    cursor.execute('INSERT INTO HKU (huisID, kamerID, userId) VALUES (?, ?, ?)',
                   (huis_id, kamer_id, current_user_id))

    # Commit the changes and close the connection
    conn.commit()
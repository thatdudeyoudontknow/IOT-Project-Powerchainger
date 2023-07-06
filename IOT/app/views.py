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


from app.models import User , Kamer, Huis, HKU, Vrienden
from app.forms import RegistrationForm, LoginForm, HuisForm, KamerForm


@app.route("/")
@login_required
def home():
    return render_template("public/home.html", name=current_user)

@app.route("/graph")
@login_required
def graph():
    return render_template("public/graph.html", name=current_user)




@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'Je bent nu uitgelogd!', 'success')
    return redirect(url_for('login'))


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

import traceback

@app.route('/huisconfig', methods=['GET', 'POST'])
@login_required
def huisconfig():
    user = current_user  # Assuming you have a way to access the current user

    # Retrieve the user's data from the database
    huis_data = Huis.query.filter_by(userID=user.id).first()
    kamer_data = Kamer.query.filter_by(userID=user.id).first()

    # Create form instances and pass the retrieved data to prefill the fields
    form = HuisForm(obj=huis_data)
    kamer_form = KamerForm(obj=kamer_data)

    if form.validate_on_submit() and kamer_form.validate_on_submit():
        try:
            # Update the existing huis instance if it exists
            if huis_data:
                huis_data.huisnaam= form.huisnaam.data
                huis_data.woonplaats = form.woonplaats.data
                huis_data.huisnummer = form.huisnummer.data
                huis_data.toevoeging = form.toevoeging.data
                huis_data.straat = form.straat.data
                huis_data.postcode = form.postcode.data
            else:
                # Create a new huis instance
                huis = Huis(
                    huisnaam=form.huisnaam.data,
                    woonplaats=form.woonplaats.data,
                    huisnummer=form.huisnummer.data,
                    toevoeging=form.toevoeging.data,
                    straat=form.straat.data,
                    postcode=form.postcode.data
                )
                db.session.add(huis)

            # Update the existing kamer instance if it exists
            if kamer_data:
                kamer_data.huisnummer = kamer_form.huisnummer.data
                kamer_data.kamernaam = kamer_form.kamernaam.data
            else:
                # Create a new kamer instance
                kamer = Kamer(
                    huisnummer=kamer_form.huisnummer.data,
                    kamernaam=kamer_form.kamernaam.data
                )
                db.session.add(kamer)

            db.session.commit()
            flash('De registratie is gelukt', 'success')
        except Exception as e:
            # Log the error message and traceback
            traceback.print_exc()
            flash('Er is een fout opgetreden bij het opslaan van de gegevens', 'error')
            return redirect(url_for('huisconfig'))  # Redirect the user to the form page

    return render_template('public/huisconfig.html', form=form, kamer_form=kamer_form, name=current_user)


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
@login_required
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
@login_required
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
@login_required
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
@login_required
def get_total_vrienden():
    # Get the absolute path of the database file in the current directory
    database_path = os.path.join(os.path.dirname(__file__), 'data.sqlite')

    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Retrieve the userIDs for the current user's friends
    cursor.execute("SELECT vriendenID, userID FROM vrienden WHERE userID = ?", (current_user.id,))
    userIDs = cursor.fetchall()

    total_verbruik_per_user = {}

    # Execute a query to retrieve the sum of verbruik values for each user and the current day
    query = """
        SELECT user.username, SUM(verbruik.verbruik)
        FROM verbruik
        JOIN user ON verbruik.userID = user.id
        WHERE verbruik.huisID IN (SELECT huisID FROM HKU WHERE userID IN ({user_ids_placeholder}))
            AND DATE(verbruik.datetime) = DATE('now', 'localtime')
        GROUP BY verbruik.userID
    """.format(user_ids_placeholder=','.join('?' for _ in userIDs))

    # Flatten the list of userIDs for use as query parameters
    userIDs_flat = [user_id for user_id, _ in userIDs]

    cursor.execute(query, userIDs_flat)  # Pass the userIDs_flat as parameters

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
def vriendenzien():

    vriend = Vrienden.query.filter_by(userID=current_user.id).all()
    

    return render_template('vrienden.html',name=current_user, vriend=vriend)


# -----------------------------------------------------------------------------------
# verwijder vrienden
@app.route('/remove_friends/<vriend_id>')
@login_required
def remove_friends(vriend_id):
    # Display the vriend_id on the remove_friends page
    return "Friend with ID {} has been successfully removed.".format(vriend_id)



# -----------------------------------------------------------------------------------
# huidig verbruik van de huidige gebruiker
@app.route('/huidig_verbruik')
@login_required
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
@login_required
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
@login_required
def process_users():
    userID = current_user.id
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
# zorg dat de vriendverzoek word weergegeven van de database
@app.route('/competitie')
@login_required
def competitie():
    userID = current_user.id
    
    # Connect to the SQLite database
    database_path = os.path.join(os.path.dirname(__file__), 'data.sqlite')
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Retrieve the friend requests for the current user based on vriendenID
    cursor.execute("""
        SELECT u.username AS inviter_username, v.verzoekID, v.status
        FROM verzoeken v
        JOIN user u ON u.id = v.userID
        WHERE v.vriendenID = ? and v.status = "pending"
    """, (userID,))
    columns = [column[0] for column in cursor.description]
    invitations = [dict(zip(columns, row)) for row in cursor.fetchall()]
    print(invitations)

    # Close the database connection
    conn.close()
    
    # Render the template and pass the invitations and current_user to it
    return render_template('public/competitie.html', invitations=invitations, name=current_user)


# -----------------------------------------------------------------------------------
# zorg dat de vriendverzoek ontvangen word en geacepteerd of afgeslagen kan worden
@app.route('/process_invitation', methods=['POST'])
@login_required
def process_invitation():
    # Get the form data
    verzoek_id = request.form['verzoek_id']
    action = request.form['action']

    # Connect to the SQLite database
    database_path = os.path.join(os.path.dirname(__file__), 'data.sqlite')
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    if action == 'accept':
        # Perform the necessary actions to accept the invitation
        inviter_id = accept_invitation(cursor, verzoek_id, current_user.id)
    elif action == 'decline':
        # Perform the necessary actions to decline the invitation
        decline_invitation(cursor, verzoek_id)

    # Commit the changes to the database
    conn.commit()

    # Close the database connection
    conn.close()

    return redirect('competitie')


def accept_invitation(cursor, verzoek_id, current_user_id):
    # Fetch the inviter's user ID from the verzoeken table
    cursor.execute("SELECT userID FROM verzoeken WHERE verzoekID = ?", (verzoek_id,))
    inviter_id = cursor.fetchone()[0]

    # Perform the necessary actions to accept the invitation
    # Update the vrienden table to add the friendship
    cursor.execute("INSERT INTO vrienden (userID, vriendenID) VALUES (?, ?)", (inviter_id, current_user_id ))
    cursor.execute("INSERT INTO vrienden (userID, vriendenID) VALUES (?, ?)", (current_user_id, inviter_id ))

    # Remove the invitation from the verzoeken table
    cursor.execute("DELETE FROM verzoeken WHERE verzoekID = ?", (verzoek_id,))

    # Return the inviter's ID
    return inviter_id


def decline_invitation(cursor, verzoek_id):
    # Perform the necessary actions to decline the invitation
    # Update the status column in the verzoeken table to 'declined'
    cursor.execute("UPDATE verzoeken SET status = 'declined' WHERE verzoekID = ?", (verzoek_id,))


# -----------------------------------------------------------------------------------
# zorg dat de data in hku word gezet
@app.route('/insert_hku', methods=['POST'])
@login_required
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

if __name__ == '__main__':
    app.run()

@app.route("/Vrienden")
@login_required
def vrienden():
        
    vriend = Vrienden.query.filter_by(userID=current_user.id).all()
    return render_template('public/vrienden.html',name=current_user, vriend=vriend)
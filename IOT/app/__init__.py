#init.py is de dunder van onze app. 
#als de app 'opstart' is dit het bestand wat aangeroepen wordt.

#in deze regel importeren we de module flask
from flask import Flask


#in deze regel defineren we app als een instantie van de Flask-klasse.
app=Flask(__name__)

#Door de regel app = Flask(__name__) te schrijven, maken we een nieuwe -
# instantie van de Flask-klasse aan en slaan we deze op in de variabele app. 
# Deze instantie wordt gebruikt om onze Flask-applicatie te configureren en te runnen. 
# De parameter __name__ geeft aan dat we de huidige module (init.py) -
# als de naam van de applicatie gebruiken. Dit is belangrijk omdat Flask -
# verschillende paden en locaties zal gebruiken op basis van de naam van de module waarin het wordt uitgevoerd.



# Hier importeren we de "views" module van onze app
from app import views

# Door het importeren van de "views" module -
# zorgen we ervoor dat de routes en views in dat bestand -
# worden uitgevoerd wanneer de app wordt opgestart. 
# Dit stelt ons in staat om de juiste routes en functionaliteit aan de app toe te voegen.


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash(u'Je bent nu uitgelogd!', 'success')
#     return redirect(url_for('index'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         print(user)
#         if user is not None and user.check_password(form.password.data):
#             login_user(user)
#             flash(u'Succesvol ingelogd.', 'success')


#             next = request.args.get('next')
#             if not next or url_parse(next).netloc != '':
#                 next = url_for('index')
#             return redirect(url_parse(next).path)
        
#         else:
#             flash(u'U email of wachtwoord is niet correct.', 'warning')     
#     return render_template('login.html', form=form) 

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user_email = User.query.filter_by(email=form.email.data).first()
#         user_username = User.query.filter_by(username=form.username.data).first()

#         if user_email:
#             flash(u'Dit emailadres is al in gebruik. Kies een ander emailadres.', 'warning')
#         elif user_username:
#             flash(u'Deze gebruikersnaam is al in gebruik. Kies een andere gebruikersnaam.', 'warning')
#         else:
#             user = User(email=form.email.data,
#                         username=form.username.data,
#                         password=form.password.data)

#             db.session.add(user)
#             db.session.commit()

#             flash(u'Dank voor de registratie. Er kan nu ingelogd worden! ', 'success')
#             return redirect(url_for('login'))

#     return render_template('register.html', form=form)
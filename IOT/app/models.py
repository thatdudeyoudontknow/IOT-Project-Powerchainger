from app.views import db, app, login_manager
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

with app.app_context():
    db.create_all()

class HKU(db.Model):
    __tablename__ ='HKU'

    huisID = db.Column(db.Integer(), primary_key=True)
    kamerID = db.Column(db.Integer())
    userId = db.Column(db.Integer())

class Huis(db.Model):
    __tablename__ ='huis'

    huisID = db.Column(db.Integer(), primary_key=True)
    userID = db.Column(db.String(100), nullable=False)
    huisnaam = db.Column(db.String(40), nullable=True)
    woonplaats = db.Column(db.String(40), nullable=False)
    huisnummer = db.Column(db.Integer(), nullable=False)
    toevoeging = db.Column(db.String(6), nullable=True)
    straat = db.Column(db.String(40), nullable=False)
    postcode = db.Column(db.String(6), nullable=False)

    def __init__(self, woonplaats, huisnummer, straat, postcode, toevoeging):
        self.woonplaats = woonplaats
        self.huisnummer = huisnummer
        self.toevoeging = toevoeging
        self.straat = straat
        self.postcode = postcode
        self.userID = current_user.id



class Kamer(db.Model):
    kamerID = db.Column(db.Integer, primary_key=True)
    kamernaam = db.Column(db.Text, nullable=True)
    huisnummer = db.Column(db.Integer, nullable=False)
    userID = db.Column(db.Integer)


    def __init__(self, kamernaam, huisnummer):
        self.kamernaam = kamernaam
        self.huisnummer = huisnummer
        self.userID = current_user.id


        
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False, index=True)
    username = db.Column(db.String(32), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(120), nullable=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Welkom, {self.username}"

class Vrienden(db.Model):
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    vriendenID = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    user = db.relationship('User', foreign_keys=[userID], backref='vrienden')
    vriend = db.relationship('User', foreign_keys=[vriendenID], backref='vriend_van')

class Verzoeken(db.Model):
    verzoekID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vriendenID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(100))

    user = db.relationship('User', foreign_keys=[userID], backref='verzoeken_verzonden')
    vriend = db.relationship('User', foreign_keys=[vriendenID], backref='verzoeken_ontvangen')

class Verbruik(db.Model):
    __tablename__ ='verbruik'

    huisID = db.Column(db.Integer, primary_key=True)
    kamerID = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, primary_key=True)
    verbruik = db.Column(db.Float())
    datetime = db.Column(db.DateTime())


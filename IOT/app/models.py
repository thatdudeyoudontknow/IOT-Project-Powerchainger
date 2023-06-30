from app.views import db, app, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

with app.app_context():
    db.create_all()

class HKU():
    __tablename__ ='HKU'

    huisID = db.Column(db.Integer(), primary_key = True )
    kamerID = db.Column(db.Integer(), ) 
    userId = db.Column(db.Integer(), )

class Huis():
    __tablename__ ='huis'

    huisId = db.Column(db.Integer(),primary_key= True)
    huisnaam = db.Column()
    verbruik_per_huis = db.Column()

class Kamer():
    __tablename__ ='kamer'

    huisId = db.Column(db.Integer())
    kamerId = db.Column(db.Integer(),primary_key= True)
    kamernaam = db.Column()

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer(),primary_key= True)
    email = db.Column(db.String(64), unique=True, nullable=False, index=True)
    username = db.Column(db.String(32), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(120), nullable=False)

    woonplaats = db.Column(db.String(40), nullable=False)
    huisnummer = db.Column(db.Integer(), nullable=False)
    toevoeging = db.Column(db.String(6), nullable=True)
    straat = db.Column(db.String(40), nullable=False)
    postcode = db.Column(db.String(6), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')



    def __init__(self, email, username,password, woonplaats,huisnummer,straat,postcode,toevoeging,role='user'):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.woonplaats = woonplaats
        self.huisnummer = huisnummer
        self.toevoeging = toevoeging
        self.straat = straat
        self.postcode = postcode
        self.role = role


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Welkom, {self.username}"


class Vrienden():
    __tablename__ ='vrienden'

    userID = db.Column()
    vriendenID = db.Column()

class Verbuik():
    __tablename__ ='verbruik'

    huisID = db.Column()
    kamerID = db.Column()
    userId = db.Column()
    verbruik = db.Column()
    datetime = db.Column()

from app import db, app, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)
Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

with app.app_context():
    db.create_all()

class HKU():
    __tablename__ ='HKU'

    huisID = db.Column(db.Integer(), Primary_key = True )
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

class User(db.Model,UserMixin):
    __tablename__ = 'user'

    userId = db.Column(db.Integer(),primary_key= True)
    gebruikersnaam = db.Column(db.String(32), nullable=False)
    wachtwoord = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(64), nullable=False)

    def __init__ (self, gebruikersnaam, wachtwoord, email):
        self.gebruikersnaam = gebruikersnaam
        self.wachtwoord = generate_password_hash(wachtwoord)
        self.email = email

    def check_password(self, wachtwoord):
        return check_password_hash(self.wachtwoord, wachtwoord)

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

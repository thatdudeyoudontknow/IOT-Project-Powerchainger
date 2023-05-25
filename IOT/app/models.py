from app import db, app


class Testdata(db.Model):
    __tablename__='testdata'
    id=db.Column(db.Integer(),primary_key = True)
    data= db.Column(db.Integer(),nullable=False, index=True)

    def __init__(self,data):
        self.data=data


with app.app_context():
    db.create_all()
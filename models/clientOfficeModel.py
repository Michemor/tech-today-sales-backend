from database import db


class ClientOffice(db.Model):

    __tablename__ = 'clientoffice'
    
    office_id = db.Column(db.Integer, primary_key=True)
    office_name = db.Column(db.String, nullable=False)
    staff_number = db.Column(db.Integer, nullable=False)
    industry_category = db.Column(db.String, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))

    def __repr__(self):
        return f'Office: {self.office_name}'

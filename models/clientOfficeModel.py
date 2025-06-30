from database import db


class ClientOffice(db.Model):

    __tablename__ = 'clientoffice'
    
    office_id = db.Column(db.Integer, primary_key=True)
    office_name = db.Column(db.String, nullable=False)
    staff_number = db.Column(db.Integer, nullable=False)
    industry_category = db.Column(db.String, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f'Office: {self.office_name}'
    
    def to_dict(self):
        return {
            'office_id': self.office_id,
            'office_name': self.office_name,
            'staff_number': self.staff_number,
            'industry_category': self.industry_category,
            'client_id': self.client_id
        }

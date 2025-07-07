from database import db
from datetime import datetime
from sqlalchemy import func


class Client(db.Model):
    """
    defines all information related to the client
    client_id: uniquely identifies the client
    fullname: name of the client
    phone_number: client's contact
    email: client's email
    job_title: the role of the client in the company
    deal_information: status of the deal
    
    Relationship: meeting_id and office_id
    """

    __tablename__ = "client"

    client_id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String, unique=True, nullable=False)
    client_contact = db.Column(db.String, unique=True, nullable=False)
    client_email = db.Column(db.String, unique=True, nullable=False)
    job_title = db.Column(db.String, unique=True, nullable=False)
    deal_information = db.Column(db.Text, unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=func.now())

    meetings = db.relationship('Meeting', backref='attends', cascade="all, delete-orphan", passive_deletes=True)
    internet = db.relationship('Internet', backref='hasinternet', cascade="all, delete-orphan", passive_deletes=True)
    buildings = db.relationship('Building', backref='owns', cascade="all, delete-orphan", passive_deletes=True)


    def __repr__(self):
        return f'Client {self.client_name} {self.timestamp}'
    
    def to_dict(self):
        return {
            'client_id': self.client_id,
            'client_name': self.client_name,
            'client_contact': self.client_contact,
            'client_email': self.client_email,
            'job_title': self.job_title,
            'deal_information': self.deal_information,
            'timestamp': self.timestamp.isoformat()
        }
    

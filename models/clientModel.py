from database import db
from datetime import datetime


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
    timestamp = db.Column(db.DateTime, default=datetime.now)
    

    meetings = db.relationship('Meeting', backref='attends', uselist=False)
    offices = db.relationship('Office', backref='owns', uselist=False)
    internet = db.relationship('Internet', backref='hasinternet', uselist=False)

    def __repr__(self):
        return f'Client {self.client_name} {self.timestamp}'
    

from database import db
from datetime import datetime
from client import Client

class Meeting(db.Model):
    meeting_id = db.Column(db.Integer, primary_key=True)
    meeting_date = db.Column(db.Datetime, nullable=False)
    meeting_location = db.Column(db.String, nullable=False)
    meeting_remarks = db.Column(db.Text, nullable=False)
    meeting_status = db.Column(db.String, nullanble=False)

    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))

    def __repr__(self):

        return f'Meeting {self.meeting_date}'


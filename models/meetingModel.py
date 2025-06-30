from database import db

class Meeting(db.Model):
    """
    Defines the columns for a meeting table
    """

    __tablename__ = 'meeting'

    meeting_id = db.Column(db.Integer, primary_key=True)
    meeting_date = db.Column(db.Date, nullable=False)
    meeting_location = db.Column(db.String, nullable=False)
    meeting_remarks = db.Column(db.Text, nullable=False)
    meetingtype = db.Column(db.String, nullable=False)  
    meeting_status = db.Column(db.String, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id', ondelete="CASCADE"))


    def __repr__(self):
        return f"Meeting \n{self.meeting_id} \n{self.meeting_date}"
    
    def to_dict(self):
        return {
            'meeting_id': self.meeting_id,
            'meeting_date': self.meeting_date.isoformat(),
            'meeting_location': self.meeting_location,
            'meeting_remarks': self.meeting_remarks,
            'meetingtype': self.meetingtype,
            'meeting_status': self.meeting_status,
            'client_id': self.client_id
        }
from database import db
from datetime import datetime
from models.clientModel import Client

class Internet(db.Model):
    """
    defines the status of the client's internet
    is_isp_connected (boolean): defines whether the client is connected to the internet
    isp_name (string): name of the isp the client is currently using
    internt_connection_type (string): the connection type as either dedicated or shared
    service_provided (string): type of service the client receives from the isp
    isp_price (decimal): amount paid by the client for the service
    deal_status (string): the status of the deal as either ongoing, terminated, closed etc
    client_id: relationship between office and client
    """

    __tablename__ = 'internet'
    
    internet_id = db.Column(db.Integer, primary_key=True)
    is_isp_connected = db.Column(db.String, nullable=False)
    isp_name = db.Column(db.String, default=None)
    internet_connection_type = db.Column(db.String, default=None)
    service_provided = db.Column(db.String, default=None)
    isp_price = db.Column(db.String, default=0)
    deal_status = db.Column(db.String, default=None)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id', ondelete="CASCADE"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'Internet status: \n{self.is_isp_connected} \n{self.timestamp}'
    
    def to_dict(self):
        return {
            'internet_id': self.internet_id,
            'is_isp_connected': self.is_isp_connected,
            'isp_name': self.isp_name,
            'internet_connection_type': self.internet_connection_type,
            'service_provided': self.service_provided,
            'isp_price': self.isp_price,
            'deal_status': self.deal_status,
            'client_id': self.client_id,
            'timestamp': self.timestamp.isoformat()
        }
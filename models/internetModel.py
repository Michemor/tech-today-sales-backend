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

    is_isp_connected = db.Column(db.Boolean, nullable=False)
    isp_name = db.Column(db.String)
    internet_connection_type = db.Column(db.String)
    service_provided = db.Column(db.String)
    isp_price = db.Column(db.Numeric)
    deal_status = db.Column(db.String)
    client_id = db.Column(db.Integer, db.ForeignKey('client_id'))
    timestamp = db.Column(db.Datetime, default=datetime.now)

    def __repr__(self):
        return f'Internet status: \n{self.is_isp_connected} \n{self.timestamp}'
    
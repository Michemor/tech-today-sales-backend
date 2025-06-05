from database import db
from datetime import datetime

class Client(db.Model):
    """
    defines all information related to the client
    client_id: uniquely identifies the client
    """
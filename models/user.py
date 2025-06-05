from engine.database import db
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    hashed_password = generate_password_hash(password)

    return hashed_password

class User(db.Model):

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    user_email = db.Column(db.String(50), unique=True, nullable=False)
    user_password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, email, password):
        self.user_name = username
        self.user_email = email
        self.user_password = hash_password(password)
    
    
    
    def __repr__(self):
        return f"<User: {self.user_id} {self.user_name}>"

    


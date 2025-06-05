from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model):
    """
    This model contains the user and creates the table for user
    userid: uniquely identifies the user
    username: the user's name
    email: stores the user's email
    password: contains the password for the user
    created_at: the time when the user was created
    """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    
    def __repr__(self):
        """
        String representation of the user object
        """
        return f"<User: {self.user_id} {self.user_name}>"
    
    def set_password(self, password):
        """
        Hashes the password of the user before storage
        """
        self.user_password = generate_password_hash(password)

    
    def check_password(self, password):
        """
        Checks if inputted password matches the one in the database
        """

        return check_password_hash(self.user_password, password)

    

    


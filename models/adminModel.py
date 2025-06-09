from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model):
    """
    Model for an admin
    """

    admin_id = db.Column(db.Integer, primary_key=True, nullable=False)
    admin_name = db.Column(db.String, nullable=False)
    admin_password = db.Column(db.String, nullable=False)

    def set_password(self, password):
        """
        Hashes the password of the user before storage
        """
        self.admin_password = generate_password_hash(password)

    
    def check_password(self, password):
        """
        Checks if inputted password matches the one in the database
        """

        return check_password_hash(self.admin_password, password)
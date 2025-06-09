from database import db

class Building(db.Model):
    """
    Model for building
    """

    __tablename__ = 'building'

    building_id = db.Column(db.Integer, primary_key=True, nullable=False)
    building_name = db.Column(db.String, nullable=False)
    is_fibre_setup = db.Column(db.Boolean, nullable=False)
    ease_of_access = db.Column(db.Integer, nullable=False)
    access_information = db.Column(db.String, nullable=False)

    offices = db.relationship('BuildingOffice', backref='building')

    def __repr__(self):

        return f'Building: {self.building_name}'
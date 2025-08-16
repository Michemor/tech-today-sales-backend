from database import db

class Building(db.Model):
    """
    Model for building
    """

    __tablename__ = 'building'

    building_id = db.Column(db.Integer, primary_key=True, nullable=False)
    building_name = db.Column(db.String, nullable=False)
    is_fibre_setup = db.Column(db.String, nullable=False)
    ease_of_access = db.Column(db.Integer, nullable=False)
    access_information = db.Column(db.String, nullable=False)
    number_offices = db.Column(db.Integer, nullable=False)

    offices = db.relationship('BuildingOffice', backref='located', cascade="all, delete-orphan", passive_deletes=True)
    clients = db.relationship('Client', backref='building', cascade="all, delete-orphan", passive_deletes=True)

    def __repr__(self):

        return f'Building: {self.building_name}'
    
    def to_dict(self):
        return {
            'building_id': self.building_id,
            'building_name': self.building_name,
            'is_fibre_setup': self.is_fibre_setup,
            'ease_of_access': self.ease_of_access,
            'access_information': self.access_information,
            'number_offices': self.number_offices,
        }
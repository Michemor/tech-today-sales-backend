from database import db

class BuildingOffice(db.Model):
    """
    Model defines the office in a building
    """

    __tablename__ = 'buildingoffice'

    office_id = db.Column(db.Integer, primary_key=True, nullable=False)
    office_name = db.Column(db.String, nullable=False)
    office_floor = db.Column(db.Integer, nullable=False)
    more_data_on_office = db.Column(db.Text, nullable=False)

    building_id = db.Column(db.Integer, db.ForeignKey('building.building_id'), nullable=False)

    def __repr__(self):
        
        return f'Office {self.office_name}'
    
    def to_dict(self):
        return {
            'office_id': self.office_id,
            'office_name': self.office_name,
            'office_floor': self.office_floor,
            'more_data_on_office': self.more_data_on_office,
            'building_id': self.building_id
        }
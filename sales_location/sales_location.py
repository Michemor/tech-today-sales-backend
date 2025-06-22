from flask import Blueprint, request, jsonify
from models.buildingModel import Building
from models.office import BuildingOffice
from database import db
from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError


"""
File containing blueprint and endpoints for sales locations
"""

location_bp = Blueprint('location_bp', __name__,)



@location_bp.route('/location', methods=['POST'])
def addLocation():
    """
    Endpoint for fetching data from form and sending to database
    """

    data = request.get_json()
    print(data)

    if not data:
        return jsonify({
            'success': False,
            'message': 'No data provided'
        }), 400

    # fetch data from json response from frontend react application
    building_name = data['building_name']
    is_fibre = data['is_fibre_setup']
    ease_access = data['ease_of_access']
    access_info = data['more_info_access']
    number_offices = data['number_of_offices']
    office_name = data['office_name']
    other_offices = data['more_offices']
    office_floor = data['office_floor']

    
    existing_building = db.session.execute(
        db.select(Building).filter_by(building_name=building_name)
    ).scalar_one_or_none()

    if existing_building:
        current_building = existing_building
        # send back response to user
        return jsonify({
            'success': False,
            'message': 'Building already exists'
        }), 400

    current_building = Building(building_name=building_name,
                                 is_fibre_setup=is_fibre,
                                 ease_of_access=ease_access,
                                 access_information=access_info,
                                 number_offices=number_offices)
        
    new_office = BuildingOffice(office_name=office_name,
                                 more_data_on_office=other_offices,
                                 office_floor=office_floor,
                                 located=current_building) 
    try:
        db.session.add(current_building)
        db.session.add(new_office)
        db.session.commit()
        # return json response to the user  for successful addition
        return jsonify({
            'success': True,
            'message': 'Location and office added successfully',
        }), 201
    
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': "Integrity error: " + str(e.orig)
        }), 400

    except DataError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': "Data error: " + str(e.orig)
        }), 400

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': "Database error: " + str(e)
        }), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': "An unexpected error occurred: " + str(e)
        }), 400


@location_bp.route('/listsites')
def listLocations():
    """
    List the offices and buildings
    """

    buildingList = []
    officeList = []

    buildings = db.session.execute(db.select(Building).order_by(Building.building_id)).scalars().all()
    offices = db.session.execute(db.select(BuildingOffice).order_by(BuildingOffice.office_id)).scalars().all()

    for building in buildings:
        buildingList.append(building.to_dict())
    
    for office in offices:
        officeList.append(office.to_dict())

    return jsonify({
        'success': True,
        'message': "Locations and Buildings fetched successfully",
        'buildings': buildingList,
        'offices': officeList
    }), 200
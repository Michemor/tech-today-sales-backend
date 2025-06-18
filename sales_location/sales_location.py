from flask import Blueprint, request, jsonify
from models.buildingModel import Building
from models.office import BuildingOffice
from database import db
from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError
import json

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

    response = {
        'success': False,
        'message': "Location added successfully"
    }

    if not data:
        response['message'] = "No data provided"
        return (jsonify(response), 400)
    # fetch data from json response from frontend react application


    building_name = data.get('building_name')
    is_fibre = data.get('is_fibre_setup')
    ease_access = data.get('ease_of_access')
    access_info = data.get('more_info_access')
    number_offices = data.get('number_of_offices')
    office_name = data.get('office_name')
    other_offices = data.get('more_offices')
    office_floor = data.get('office_floor')

    
    existing_building = db.session.execute(
        db.select(Building).filter_by(building_name=building_name)
    ).scalar_one_or_none()

    if existing_building:
        current_building = existing_building
        # send back response to user
        response['success'] = False
        response['message'] = "Building already exists, adding office to existing building"
        return (jsonify(response), 400)

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
        response['success'] = True
        response['message'] = "Location added successfully"
        return (jsonify(response), 200)
    
    except IntegrityError as e:
        db.session.rollback()
        response['message'] = "Integrity error: " + str(e.orig)
        return (jsonify(response), 400)
    
    except DataError as e:
        db.session.rollback()
        response['message'] = "Data error: " + str(e.orig)
        return (jsonify(response), 400)

    except SQLAlchemyError as e:
        db.session.rollback()
        response['message'] = "Database error: " + str(e)
        return (jsonify(response), 400)
    
    except Exception as e:
        db.session.rollback()
        response['message'] = "An unexpected error occurred: " + str(e)
        return (jsonify(response), 400)


@location_bp.route('/listsites')
def listLocations():
    """
    List the offices and buildings
    """

    buildings = db.session.execute(db.select(Building).order_by(Building.building_id)).scalars().all()
    offices = db.session.execute(db.select(BuildingOffice).order_by(BuildingOffice.office_id)).scalars().all()

    return render_template('lists.html', buildings=buildings, offices=offices)
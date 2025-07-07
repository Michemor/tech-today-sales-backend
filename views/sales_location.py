from flask import Blueprint, request, jsonify
from models.buildingModel import Building
from models.office import BuildingOffice
from database import db
from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError


"""
File containing blueprint and endpoints for sales locations
"""

location_bp = Blueprint(
    "location_bp",
    __name__,
)


@location_bp.route("/location", methods=["POST"])
def addLocation():
    """
    Endpoint for fetching data from form and sending to database
    """

    data = request.get_json()
    print(data)

    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    # fetch data from json response from frontend react application
    building_name = data["building_name"]
    is_fibre = data["is_fibre_setup"]
    ease_access = data["ease_of_access"]
    access_info = data["more_info_access"]
    number_offices = data["number_of_offices"]
    office_name = data["office_name"]
    
     # office information
    office_name = data.get('office_name')
    staff_number = data.get('number_staff')
    industry_category = data.get('industry')
    other_offices = data["more_offices"]
    office_floor = data["office_floor"]

    existing_building = db.session.execute(
        db.select(Building).filter_by(building_name=building_name)
    ).scalar_one_or_none()

    if existing_building:
        current_building = existing_building
        # send back response to user
        return jsonify({"success": False, "message": "Building already exists"}), 400

    current_building = Building(
        building_name=building_name,
        is_fibre_setup=is_fibre,
        ease_of_access=ease_access,
        access_information=access_info,
        number_offices=number_offices,
    )

    new_office = BuildingOffice(
        office_name=office_name,
        more_data_on_office=other_offices,
        office_floor=office_floor,
        located=current_building,
    )
    try:
        db.session.add(current_building)
        db.session.add(new_office)
        db.session.commit()
        # return json response to the user  for successful addition
        return (
            jsonify(
                {
                    "success": True,
                    "message": "Location and office added successfully",
                }
            ),
            201,
        )

    except IntegrityError as e:
        db.session.rollback()
        return (
            jsonify({"success": False, "message": "Integrity error: " + str(e.orig)}),
            400,
        )

    except DataError as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "Data error: " + str(e.orig)}), 400

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "Database error: " + str(e)}), 400

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {"success": False, "message": "An unexpected error occurred: " + str(e)}
            ),
            400,
        )


@location_bp.route("/locations/buildings", methods=["GET"])
def getBuilding():
    """
    Endpoint to get all buildings
    """

    buildings = (
        db.session.execute(db.select(Building).order_by(Building.building_id))
        .scalars()
        .all()
    )

    if not buildings:
        return jsonify({"success": False, "message": "No buildings found"}), 404

    buildingList = [building.to_dict() for building in buildings]

    for building in buildings:
        print(building.offices)
    
    

    return (
        jsonify(
            {
                "success": True,
                "message": "Buildings fetched successfully",
                "buildings": buildingList,
            }
        ),
        200,
    )


@location_bp.route("/locations/offices", methods=["GET"])
def getofficeBuilding():
    """
    Endpoint to get all offices in a building by building ID
    """

    offices = (
        db.session.execute(db.select(BuildingOffice).order_by(BuildingOffice.office_id))
        .scalars()
        .all()
    )

    if not offices:
        return (
            jsonify(
                {"success": False, "message": "No offices found for this building"}
            ),
            404,
        )

    officeList = [office.to_dict() for office in offices]

    return (
        jsonify(
            {
                "success": True,
                "message": "Offices fetched successfully",
                "offices": officeList,
            }
        ),
        200,
    )


@location_bp.route("/locations/building/<int:building_id>", methods=["DELETE"])
def deleteBuilding(building_id):
    """
    Endpoint to delete a building by ID along with all related offices
    """

    building = db.session.execute(
        db.select(Building).filter_by(building_id=building_id)
    ).scalar_one_or_none()

    if not building:
        return jsonify({"success": False, "message": "Building not found"}), 404

    try:
        # Delete related offices first to avoid foreign key constraint violations
        offices = (
            db.session.execute(
                db.select(BuildingOffice).filter_by(building_id=building_id)
            )
            .scalars()
            .all()
        )

        for office in offices:
            db.session.delete(office)

        # Finally delete the building
        db.session.delete(building)
        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Building and all related offices deleted successfully",
                }
            ),
            200,
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "Database error: " + str(e)}), 500


@location_bp.route("/locations/building/<int:building_id>", methods=["PUT"])
def updateBuilding(building_id):
    """
    Endpoint to update a building by ID
    """

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    building = db.session.execute(
        db.select(Building).filter_by(building_id=building_id)
    ).scalar_one_or_none()

    if not building:
        return jsonify({"success": False, "message": "Building not found"}), 404

    allowed_fields = [
        "building_name",
        "is_fibre_setup",
        "ease_of_access",
        "access_information",
        "number_offices",
    ]

    valid_fields = {key: value for key, value in data.items() if key in allowed_fields}
    for field, value in valid_fields.items():
        setattr(building, field, value)

    try:
        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Building updated successfully",
                    "building": building.to_dict(),
                }
            ),
            200,
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "Database error: " + str(e)}), 500


@location_bp.route("/locations/office/<int:office_id>", methods=["DELETE"])
def deleteOffice(office_id):
    """
    Endpoint for deleting office
    """
    office = db.session.execute(
        db.select(BuildingOffice).filter_by(office_id=office_id)
    ).scalar_one_or_none()

    if not office:
        return jsonify({"success": False, "message": "Office not found"}), 404

    try:
        db.session.delete(office)
        db.session.commit()
        return jsonify({"success": True, "message": "Office deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "Database error: " + str(e)}), 500


@location_bp.route("/locations/office/<int:office_id>", methods=["PUT"])
def updateOffice(office_id):
    """Update office details"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    office = db.session.execute(
        db.select(BuildingOffice).filter_by(office_id=office_id)
    ).scalar_one_or_none()

    if not office:
        return jsonify({"success": False, "message": "Office not found"}), 404

    allowed_fields = ["office_name", "more_data_on_office", "office_floor"]

    valid_fields = {key: value for key, value in data.items() if key in allowed_fields}
    for field, value in valid_fields.items():
        setattr(office, field, value)

    try:
        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Office updated successfully",
                    "office": office.to_dict(),
                }
            ),
            200,
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "Database error: " + str(e)}), 500

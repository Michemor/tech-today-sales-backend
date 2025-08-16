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


@location_bp.route("/locations/offices/<int:building_id>", methods=["GET"])
def getOffice(building_id):
    """
    Endpoint to get all offices in a building by building ID
    """

    offices = db.session.execute(db.select(BuildingOffice).filter_by(building_id=building_id)).scalars().all()

    if not offices:
        return (
            jsonify(
                {"success": False, "message": "No offices found for this building"}
            ),
            404,
        )
    
    offices = [office.to_dict() for office in offices]

    print("Offices:\n", offices)

    return (
        jsonify(
            {
                "success": True,
                "message": "Offices fetched successfully",
                "offices": offices,
            }
        ),
        200,
    )

@location_bp.route("/locations/offices", methods=["GET"])
def getOffices():
    """
    Endpoint to fetch all offices
    """
    offices = db.session.execute(db.select(BuildingOffice).order_by(BuildingOffice.office_id)).scalars().all()

    if not offices:
        return jsonify({"success": False, "message": "No offices found"}), 404

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

@location_bp.route("/locations/building/<building_id>", methods=["DELETE"])
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


@location_bp.route("/locations/offices/names", methods=["GET"])
def getOfficeNames():
    """
    Endpoint for fetching office names
    """
    names = db.session.execute(
        db.select(BuildingOffice.office_name)
    ).scalars().all()

    if not names:
        return jsonify({"success": False, "message": "No office names found"}), 404

    return (
        jsonify(
            {
                "success": True,
                "offices_names": names,
            }
        ),
        200,
    )
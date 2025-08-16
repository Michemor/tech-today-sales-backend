from xmlrpc import client
from flask import Blueprint, request, jsonify
from models.clientModel import Client
from models.userModel import User
from database import db
from models.internetModel import Internet
from models.meetingModel import Meeting
from models.office import BuildingOffice
from models.buildingModel import Building
from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError
from sqlalchemy import func

"""
This file contains routes for entering client data 
"""

client_bp = Blueprint("client_bp", __name__)


@client_bp.route("/", methods=["POST"])
def userLogin():
    """
    Endpoint for user to login in to the system
    """
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    name = data.get("user_name")
    password = data.get("password")

    existing_user = db.session.execute(
        db.select(User).filter_by(user_name=name)
    ).scalar_one_or_none()
    if existing_user and existing_user.check_password(password):
        return jsonify({"success": True, "message": "Login successful"}), 200
    else:
        return (
            jsonify({"success": False, "message": "Invalid username or password"}),
            401,
        )


@client_bp.route("/salesdetails", methods=["POST"])
def addSales():
    """
    This endpoint if for fetching user data and saving it in the database
    """

    data = request.get_json()
    if not data:
        return (jsonify({"success": False, "message": "No data provided"}), 400)

    try:
        building_name = data.get("building_name")
        building = db.session.execute(
            db.select(Building).filter_by(building_name=building_name)
        ).scalar_one_or_none()

        if not building:
            building = Building(
                building_name=data.get("building_name"),
                is_fibre_setup=data.get("is_fibre_setup"),
                ease_of_access=data.get("ease_of_access"),
                access_information=data.get("more_info_access"),
                number_offices=data.get("number_offices"),
            )
        db.session.add(building)
        db.session.flush()

        office_name = data.get("office_name")
        office_exists = db.session.execute(
            db.select(BuildingOffice).filter_by(office_name=office_name)
        ).scalar_one_or_none()

        if not office_exists:
            office_exists = BuildingOffice(
                office_name=office_name,
                office_floor=data.get("office_floor"),
                staff_number=data.get("number_staff"),
                industry_category=data.get("industry"),
                more_data_on_office=data.get("more_offices"),
                located=building,
            )

        db.session.add(office_exists)
        # client information fetched from frontend
        client = Client(
            client_name=data.get("client_name"),
            client_contact=data.get("contact"),
            client_email=data.get("client_email"),
            job_title=data.get("job"),
            deal_information=data.get("deal_info"),
            office=office_exists,
            building=building
        )
        db.session.add(client)

        # meeting information fetched from frontend
        meeting = Meeting(
            meeting_date=data.get("meetingDate"),
            meeting_location=data.get("meetingLocation"),
            meetingtype=data.get("meetingType"),
            meeting_remarks=data.get("meetingRemarks"),
            meeting_status=data.get("meetingStatus"),
            attends=client
        )
        db.session.add(meeting)

        # internet information
        internet = Internet(
            is_isp_connected=data.get("is_connected"),
            isp_name=data.get("isp_name"),
            internet_connection_type=data.get("connection_type"),
            service_provided=data.get("product"),
            isp_price=data.get("net_price"),
            deal_status=data.get("deal_status"),
            hasinternet=client
        )
        db.session.add(internet)

        print(
            "=======Building Details:\n {}\n ======Office Details:\n {}".format(
                building.to_dict(), office_exists.to_dict()
            )
        )

        db.session.commit()
        return (
            jsonify(
                {"success": True, "message": "Client information added successfully"}
            ),
            201,
        )

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Integrity error: {e.orig}"})

    except DataError as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Data error: {e.orig}"}), 400

    except SQLAlchemyError as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "success": False,
                    "message": f"Unexpected database error occured \n {e}",
                }
            ),
            500,
        )

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {"success": False, "message": f"Failure in adding the information {e}"}
            ),
            500,
        )


@client_bp.route("/meetings", methods=["GET"])
def get_meetings():
    """
    Displays a lists of clients from the database
    """
    meeting_data = []

    meeting_list = (
        db.session.execute(db.select(Meeting).order_by(Meeting.meeting_id))
        .scalars()
        .all()
    )

    for meeting in meeting_list:
        meeting_data.append(meeting.to_dict())

    return (
        jsonify(
            {
                "success": True,
                "meetings": meeting_data,
            }
        ),
        200,
    )


@client_bp.route("/clients", methods=["GET"])
def get_clients():
    """
    Endpoint to get all clients
    """

    clientsDict = []

    clients = (
        db.session.execute(db.select(Client).order_by(Client.client_id)).scalars().all()
    )

    for client in clients:
        clientsDict.append(client.to_dict())

    return jsonify({"success": True, "clients": clientsDict}), 200


@client_bp.route("/internet", methods=["GET"])
def get_internet():
    """
    Endpoint to get all internet statuses
    """

    internet = (db.session.execute(db.select(Internet).order_by(Internet.internet_id))
                .scalars()
                .all())

    internet_list = [i.to_dict() for i in internet]

    return jsonify({"success": True, "internet": internet_list}), 200


@client_bp.route("/offices", methods=["GET"])
def get_offices():
    """
    Endpoint to get all client offices
    """
    offices = (
        db.session.execute(db.select(BuildingOffice).order_by(BuildingOffice.office_id))
        .scalars()
        .all()
    )
    office_list = [office.to_dict() for office in offices]

    return jsonify({"success": True, "offices": office_list}), 200


@client_bp.route("/update", methods=["POST"])
def update_client_data():
    """Updates the client data in the database.

    Returns:
        json: A JSON response indicating success or failure.
    """

    # updates data from client depending on the category sent from the frontend
    data = request.get_json()

    print(f"Received data for update\n: {data}")

    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    category = data.get("category")
    id = data.get("client_id")
    value = data.get("value")
    field = data.get("field")
    context = data.get("clientData")

    print("\n\n=============Context data sent frpm frontend:\n", context)

    # if not category or not id or not value or not field:
    # return (
    # jsonify({"success": False, "message": "Missing required fields"}),
    # 400,
    # )

    try:
        if category == "client":
            client = db.session.execute(
                db.select(Client).filter_by(client_id=context["client"]["client_id"])
            ).scalar_one_or_none()
            if not client:
                return jsonify({"success": False, "message": "Client not found"}), 404
            setattr(client, field, value)

        elif category == "meeting":
            meeting = db.session.execute(
                db.select(Meeting).filter_by(
                    meeting_id=context["meeting"]["meeting_id"]
                )
            ).scalar_one_or_none()
            if not meeting:
                return jsonify({"success": False, "message": "Meeting not found"}), 404
            setattr(meeting, field, value)

        elif category == "internet":
            internet = db.session.execute(
                db.select(Internet).filter_by(
                    internet_id=context["internet"]["internet_id"]
                )
            ).scalar_one_or_none()
            if not internet:
                return (
                    jsonify({"success": False, "message": "Internet record not found"}),
                    404,
                )
            setattr(internet, field, value)

        elif category == "building":
            building = db.session.execute(
                db.select(Building).filter_by(
                    building_id=context["building"]["building_id"]
                )
            ).scalar_one_or_none()
            if not building:
                return (
                    jsonify({"success": False, "message": "Building record not found"}),
                    404,
                )
            setattr(building, field, value)

        elif category == "office":
            office = db.session.execute(
                db.select(BuildingOffice).filter_by(
                    office_id=context["office"]["office_id"]
                )
            ).scalar_one_or_none()
            if not office:
                return (
                    jsonify({"success": False, "message": "Office record not found"}),
                    404,
                )
            setattr(office, field, value)

        else:
            return jsonify({"success": False, "message": "Invalid category"}), 400

        db.session.commit()
        return (
            jsonify({"success": True, "message": f"{category} updated successfully"}),
            200,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Database error: {e}"}), 500


@client_bp.route("/client/<client_id>", methods=["DELETE"])
def deleteClient(client_id):
    """
    Endpoint to delete a client by ID along with all related records
    """
    client = db.session.execute(
        db.select(Client).filter_by(client_id=client_id)
    ).scalar_one_or_none()

    if not client:
        return jsonify({"success": False, "message": "Client not found"}), 404

    try:
        # Delete related records in the correct order to avoid foreign key constraint violations
        # Step 1: Get all buildings for this client
        buildings = (
            db.session.execute(db.select(Building).filter_by(client_id=client_id))
            .scalars()
            .all()
        )

        # Step 2: Delete all offices in all buildings owned by this client
        for building in buildings:
            offices = (
                db.session.execute(
                    db.select(BuildingOffice).filter_by(
                        building_id=building.building_id
                    )
                )
                .scalars()
                .all()
            )
            for office in offices:
                db.session.delete(office)

        # Step 3: Delete all buildings
        for building in buildings:
            db.session.delete(building)

        # Step 4: Delete related internet records
        internet_records = (
            db.session.execute(db.select(Internet).filter_by(client_id=client_id))
            .scalars()
            .all()
        )
        for internet in internet_records:
            db.session.delete(internet)

        # Step 5: Delete related meetings
        meetings = (
            db.session.execute(db.select(Meeting).filter_by(client_id=client_id))
            .scalars()
            .all()
        )
        for meeting in meetings:
            db.session.delete(meeting)

        # Step 6: Finally delete the client
        db.session.delete(client)
        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Client and all related records deleted successfully",
                }
            ),
            200,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Database error: {e}"}), 500


@client_bp.route("/meeting/<meeting_id>", methods=["DELETE"])
def deleteMeeting(meeting_id):
    """
    Endpoint to delete a meeting by ID
    """
    meeting = db.session.execute(
        db.select(Meeting).filter_by(meeting_id=meeting_id)
    ).scalar_one_or_none()

    if not meeting:
        return jsonify({"success": False, "message": "Meeting not found"}), 404

    try:
        db.session.delete(meeting)
        db.session.commit()
        return (
            jsonify({"success": True, "message": "Meeting deleted successfully"}),
            200,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Database error: {e}"}), 500


@client_bp.route("/internet/<internet_id>", methods=["DELETE"])
def deleteInternet(internet_id):
    """
    Endpoint to delete internet information by ID
    """
    internet = db.session.execute(
        db.select(Internet).filter_by(internet_id=internet_id)
    ).scalar_one_or_none()

    if not internet:
        return (
            jsonify({"success": False, "message": "Internet information not found"}),
            404,
        )

    try:
        db.session.delete(internet)
        db.session.commit()
        return (
            jsonify(
                {
                    "success": True,
                    "message": "Internet information deleted successfully",
                }
            ),
            200,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Database error: {e}"}), 500


@client_bp.route("/office/<office_id>", methods=["DELETE"])
def deleteOffice(office_id):
    """
    Endpoint to delete office information by ID
    """
    office = db.session.execute(
        db.select(BuildingOffice).filter_by(office_id=office_id)
    ).scalar_one_or_none()

    if not office:
        return (
            jsonify({"success": False, "message": "Office information not found"}),
            404,
        )

    try:
        db.session.delete(office)
        db.session.commit()
        return (
            jsonify(
                {"success": True, "message": "Office information deleted successfully"}
            ),
            200,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Database error: {e}"}), 500


@client_bp.route("/sales", methods=["GET"])
def get_sales():
    """
    Endpoint to get sales data for all clients
    """
    clients = db.session.execute(db.select(Client)).scalars().all()

    sales_data = []

    for client in clients:
        # Get all meetings for this client
        meetings = (
            db.session.execute(db.select(Meeting).filter_by(client_id=client.client_id))
            .scalars()
            .all()
        )

        # Get all internet records for this client
        internet_records = (
            db.session.execute(
                db.select(Internet).filter_by(client_id=client.client_id)
            )
            .scalars()
            .all()
        )

        # Get all buildings for this client
        buildings = (
            db.session.execute(
                db.select(Building).filter_by(building_id=client.building_id)
            ).scalars().all()
        )

        # Get all offices for all buildings of this client
        offices  = (
            db.session.execute(
                db.select(BuildingOffice).filter_by(office_id=client.office_id)
            ).scalars().all()
        )

        # Combine all data for this client
        client_data = {
            "client": client.to_dict(),
            "meetings": [meeting.to_dict() for meeting in meetings],
            "internet_records": [internet.to_dict() for internet in internet_records],
            "buildings": [building.to_dict() for building in buildings],
            "offices": [office.to_dict() for office in offices],
            "total_meetings": len(meetings),
            "total_internet_records": len(internet_records),
        }

        sales_data.append(client_data)

    return (
        jsonify(
            {
                "success": True,
                "message": "Sales data retrieved successfully for all clients",
                "total_clients": len(sales_data),
                "sales_data": sales_data,
            }
        ),
        200,
    )


@client_bp.route("/sales/<int:user_id>", methods=["GET"])
def get_client_data(user_id):
    """
    Endpoint to get sales data:
    - If user_id is provided: returns data for that specific user
    - If no user_id: returns data for all users
    """

    # If user_id is provided, return data for specific user
    user = db.session.get(Client, user_id)

    print("---User data: ", user)

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    # Get all meetings for this user
    user_meeting = db.session.execute(
        db.select(Meeting).filter_by(client_id=user_id)
    ).scalar_one_or_none()
    # Get all internet records for this user
    user_internet = db.session.execute(
        db.select(Internet).filter_by(client_id=user_id)
    ).scalar_one_or_none()

    user_building_id = user.building_id
    # Get all buildings for this user
    user_building = db.session.execute(
        db.select(Building).filter_by(building_id=user_building_id)
    ).scalar_one_or_none()
    # Get all offices for all buildings of this user
    user_office = db.session.execute(
        db.select(BuildingOffice).filter_by(office_id=user.office_id)
    ).scalar_one_or_none()
    # Combine all data for this client
    client_data = {
        "client": user.to_dict(),
        "meeting": user_meeting.to_dict() if user_meeting else None,
        "internet": user_internet.to_dict() if user_internet else None,
        "building": user_building.to_dict() if user_building else None,
        "office": user_office.to_dict() if user_office else None,
    }
    print(f"======={user.client_name} data retrieved successfully\n {client_data}")
    return (
        jsonify(
            {
                "success": True,
                "message": f"Sales data retrieved for client {user.client_name}",
                "client_data": client_data,
            }
        ),
        200,
    )


@client_bp.route("/clear-all-data", methods=["DELETE"])
def clear_all_data():
    """
    Utility endpoint to clear all data from all tables while respecting foreign key constraints
    WARNING: This will delete ALL data in the database!
    """
    try:
        # Delete in the correct order to respect foreign key constraints

        # Step 1: Delete all offices first (they depend on buildings)
        offices = db.session.execute(db.select(BuildingOffice)).scalars().all()
        for office in offices:
            db.session.delete(office)

        # Step 2: Delete all buildings (they depend on clients)
        buildings = db.session.execute(db.select(Building)).scalars().all()
        for building in buildings:
            db.session.delete(building)

        # Step 3: Delete all internet records (they depend on clients)
        internet_records = db.session.execute(db.select(Internet)).scalars().all()
        for internet in internet_records:
            db.session.delete(internet)

        # Step 4: Delete all meetings (they depend on clients)
        meetings = db.session.execute(db.select(Meeting)).scalars().all()
        for meeting in meetings:
            db.session.delete(meeting)

        # Step 5: Finally delete all clients
        clients = db.session.execute(db.select(Client)).scalars().all()
        for client in clients:
            db.session.delete(client)

        db.session.commit()

        return (
            jsonify({"success": True, "message": "All data cleared successfully"}),
            200,
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Database error: {e}"}), 500


@client_bp.route("/client/<client_id>/complete", methods=["GET"])
def get_complete_client_data(client_id):
    """
    Endpoint to get complete data for a specific client including all related records
    """
    # Get the client
    client = db.session.execute(
        db.select(Client).filter_by(client_id=client_id)
    ).scalar_one_or_none()

    if not client:
        return jsonify({"success": False, "message": "Client not found"}), 404

    # Get all meetings for this client
    meetings = (
        db.session.execute(db.select(Meeting).filter_by(client_id=client_id))
        .scalars()
        .all()
    )

    # Get all internet records for this client
    internet_records = (
        db.session.execute(db.select(Internet).filter_by(client_id=client_id))
        .scalars()
        .all()
    )

    # Get all buildings for this client with their offices
    buildings = (
        db.session.execute(db.select(Building).filter_by(client_id=client_id))
        .scalars()
        .all()
    )

    buildings_with_offices = []
    for building in buildings:
        offices = (
            db.session.execute(
                db.select(BuildingOffice).filter_by(building_id=building.building_id)
            )
            .scalars()
            .all()
        )

        building_dict = building.to_dict()
        building_dict["offices"] = [office.to_dict() for office in offices]
        buildings_with_offices.append(building_dict)

    # Combine all data
    complete_data = {
        "client": client.to_dict(),
        "meetings": [meeting.to_dict() for meeting in meetings],
        "internet_records": [internet.to_dict() for internet in internet_records],
        "buildings": buildings_with_offices,
        "summary": {
            "total_meetings": len(meetings),
            "total_buildings": len(buildings),
            "total_internet_records": len(internet_records),
            "total_offices": sum(
                len(building.get("offices", [])) for building in buildings_with_offices
            ),
        },
    }

    return (
        jsonify(
            {
                "success": True,
                "message": f"Complete data retrieved for client {client.client_name}",
                "data": complete_data,
            }
        ),
        200,
    )


@client_bp.route("/count", methods=["GET"])
def count_sales():
    """
    Endpoint to get the count of all clients
    """
    try:
        client_count = db.session.execute(
            db.select(func.count(Client.client_id))
        ).scalar()

        meeting_count = db.session.execute(
            db.select(
                func.count(Meeting.meeting_id).filter(
                    Meeting.meeting_status == "Scheduled"
                )
            )
        ).scalar()

        deal_status_count = db.session.execute(
            db.select(
                func.count(Internet.internet_id).filter(
                    Internet.deal_status == "Pending"
                )
            )
        ).scalar()

        if client_count is None:
            client_count = 0

        if meeting_count is None:
            meeting_count = 0

        if deal_status_count is None:
            deal_status_count = 0
        # Log the counts for debugging
        print(
            f"Client count: {client_count}, \
              Meeting count: {meeting_count}, \
                Deal status count: {deal_status_count}"
        )
        return (
            jsonify(
                {
                    "success": True,
                    "data": {
                        "client_count": client_count,
                        "meeting_count": meeting_count,
                        "deal_status": deal_status_count,
                    },
                }
            ),
            200,
        )
    except SQLAlchemyError as e:
        return jsonify({"success": False, "message": f"Database error: {e}"}), 500


@client_bp.route("/building_names", methods=["GET"])
def get_building_name():
    """Fetches the building name from the database"""
    names = []
    buildings = (
        db.session.execute(db.select(Building).order_by(Building.building_id))
        .scalars()
        .all()
    )
    for building in buildings:
        names.append(building.building_name)

    print(f"Building names fetched: {names}")

    return jsonify({"success": True, "building_names": names}), 200


@client_bp.route("/office_names", methods=["GET"])
def get_office_name():
    """Fetches the office name from the database"""
    names = []
    offices = (
        db.session.execute(db.select(BuildingOffice).order_by(BuildingOffice.office_id))
        .scalars()
        .all()
    )
    for office in offices:
        names.append(office.office_name)

    print(f"Office names fetched: {names}")

    return jsonify({"success": True, "office_names": names}), 200

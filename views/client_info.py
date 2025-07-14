from flask import Blueprint, request, jsonify
from models.clientModel import Client
from models.userModel import User
from database import db
from models.internetModel import Internet
from models.meetingModel import Meeting
from models.office import BuildingOffice
from models.buildingModel import Building
from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError

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
def salesOffice():
    """
    This endpoint if for fetching user data and saving it in the database
    """

    data = request.get_json()
    if not data:
        return (jsonify({"success": False, "message": "No data provided"}), 400)

    # client information fetched from frontend
    client_name = data.get("client_name")
    client_contact = data.get("contact")
    client_email = data.get("client_email")
    job_title = data.get("job")
    deal_information = data.get("deal_info")

    # meeting information fetched from frontend
    date = data.get("meetingDate")
    location = data.get("meetingLocation")
    type_of_meeting = data.get("meetingType")
    remarks = data.get("meetingRemarks")
    status = data.get("meetingStatus")

    # internet information
    isp_connected = data.get("is_connected")
    isp_name = data.get("isp_name")
    net_connection_type = data.get("connection_type")
    product = data.get("product")
    net_price = data.get("net_price")
    deal_status = data.get("deal_status")

    new_client = Client(
        client_name=client_name,
        client_contact=client_contact,
        client_email=client_email,
        job_title=job_title,
        deal_information=deal_information,
    )

    new_building = Building(
        building_name=data.get("building_name"),
        is_fibre_setup=data.get("is_fibre_setup"),
        ease_of_access=data.get("ease_of_access"),
        access_information=data.get("access_information"),
        number_offices=data.get("number_offices"),
        owns=new_client,
    )

    new_office = BuildingOffice(
        office_name=data.get("office_name"),
        office_floor=data.get("office_floor"),
        staff_number=data.get("staff_number"),
        industry_category=data.get("industry_category"),
        more_data_on_office=data.get("more_data_on_office"),
        located=new_building,
    )

    new_meeting = Meeting(
        meeting_date=date,
        meeting_location=location,
        meetingtype=type_of_meeting,
        meeting_remarks=remarks,
        meeting_status=status,
        attends=new_client,
    )

    new_internet = Internet(
        is_isp_connected=isp_connected,
        isp_name=isp_name,
        internet_connection_type=net_connection_type,
        service_provided=product,
        isp_price=net_price,
        deal_status=deal_status,
        hasinternet=new_client,
    )

    try:
        db.session.add_all(
            [new_client, new_meeting, new_internet, new_building, new_office]
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
def get_internet_status():
    """
    Endpoint to get all internet statuses
    """

    internetDict = []
    internet_statuses = (
        db.session.execute(db.select(Internet).order_by(Internet.internet_id))
        .scalars()
        .all()
    )

    for internet in internet_statuses:
        internetDict.append(internet.to_dict())

    return jsonify({"success": True, "internet": internetDict}), 200


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


@client_bp.route("/client/<client_id>", methods=["PUT"])
def updateClient(client_id):
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    # Find the client first
    client = db.session.execute(
        db.select(Client).filter_by(client_id=client_id)
    ).scalar_one_or_none()

    if not client:
        return jsonify({"success": False, "message": "Client not found"}), 404

    # Define allowed fields that can be updated
    allowed_fields = [
        "client_name",
        "client_contact",
        "client_email",
        "job_title",
        "deal_information",
    ]

    # Check if at least one valid field is provided
    valid_fields = {key: value for key, value in data.items() if key in allowed_fields}

    if not valid_fields:
        return (
            jsonify(
                {"success": False, "message": "No valid fields provided for update"}
            ),
            400,
        )

    # Update only the provided valid fields
    for key, value in valid_fields.items():
        setattr(client, key, value)

    try:
        db.session.commit()
        return (
            jsonify(
                {
                    "success": True,
                    "message": "Client data updated successfully",
                    "updatedClient": client.to_dict(),
                }
            ),
            200,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Database error: {e}"}), 500


@client_bp.route("/internet/<internet_id>", methods=["PUT"])
def updateInternet(internet_id):
    """
    Endpoint to update internet information by ID
    """
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    internet = db.session.execute(
        db.select(Internet).filter_by(internet_id=internet_id)
    ).scalar_one_or_none()

    if not internet:
        return (
            jsonify({"success": False, "message": "Internet information not found"}),
            404,
        )

    # Update internet fields
    for key, value in data.items():
        setattr(internet, key, value)

    try:
        db.session.commit()
        return (
            jsonify(
                {
                    "success": True,
                    "message": "Internet information updated successfully",
                    "internet": internet.to_dict(),
                }
            ),
            200,
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Database error: {e}"}), 500


@client_bp.route("/office/<office_id>", methods=["PUT"])
def updateOffice(office_id):
    """
    Endpoint to update office information by ID
    """
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    office = db.session.execute(
        db.select(BuildingOffice).filter_by(office_id=office_id)
    ).scalar_one_or_none()

    if not office:
        return (
            jsonify({"success": False, "message": "Office information not found"}),
            404,
        )

    # Update office fields
    for key, value in data.items():
        setattr(office, key, value)

    try:
        db.session.commit()
        return (
            jsonify(
                {
                    "success": True,
                    "message": "Office information updated successfully",
                    "office": office.to_dict(),
                }
            ),
            200,
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Database error: {e}"}), 500


@client_bp.route("/meeting/<meeting_id>", methods=["PUT"])
def updateMeeting(meeting_id):
    """
    Endpoint to update meeting information by ID
    """
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    meeting = db.session.execute(
        db.select(Meeting).filter_by(meeting_id=meeting_id)
    ).scalar_one_or_none()

    if not meeting:
        return jsonify({"success": False, "message": "Meeting not found"}), 404

    # Update meeting fields
    for key, value in data.items():
        setattr(meeting, key, value)

    try:
        db.session.commit()
        return (
            jsonify(
                {
                    "success": True,
                    "message": "Meeting information updated successfully",
                    "meeting": meeting.to_dict(),
                }
            ),
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
                db.session.execute(db.select(BuildingOffice).filter_by(building_id=building.building_id))
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
def get_sales_data():
    """
    Endpoint to get all sales data including clients, meetings, internet, and offices
    """
    try:
        # Get all clients using the same pattern as other endpoints
        clients = (
            db.session.execute(db.select(Client).order_by(Client.client_id))
            .scalars()
            .all()
        )

        if not clients:
            return jsonify({"success": False, "message": "No data found"}), 404

        sales = []

        for client in clients:
            # Get meetings for this client
            meetings = (
                db.session.execute(
                    db.select(Meeting).filter_by(client_id=client.client_id)
                )
                .scalars()
                .all()
            )

            # Get internet records for this client
            internet_records = (
                db.session.execute(
                    db.select(Internet).filter_by(client_id=client.client_id)
                )
                .scalars()
                .all()
            )

            # Get buildings for this client (check if client_id column exists)
            try:
                buildings = (
                    db.session.execute(
                        db.select(Building).filter_by(client_id=client.client_id)
                    )
                    .scalars()
                    .all()
                )
            except SQLAlchemyError:
                # If client_id doesn't exist in building table, return empty list
                buildings = []

            # Build the sales data structure for each client
            sales_data = {
                "client": client.to_dict(),
                "meetings": [meeting.to_dict() for meeting in meetings],
                "internet": [internet.to_dict() for internet in internet_records],
                "buildings": [building.to_dict() for building in buildings],
                "offices": [],
            }

            # Add all offices from all buildings owned by this client
            for building in buildings:
                # Get offices for this building
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
                    office_dict = office.to_dict()
                    office_dict["building_name"] = (
                        building.building_name
                    )  # Add building name for reference
                    sales_data["offices"].append(office_dict)

            sales.append(sales_data)
            print(sales)

        return jsonify({"success": True, "sales": sales}), 200

    except SQLAlchemyError as e:
        return jsonify({"success": False, "message": f"Database error: {e}"}), 500


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
        
        return jsonify({
            "success": True,
            "message": "All data cleared successfully"
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": f"Database error: {e}"
        }), 500

from flask import Blueprint, request, jsonify
from models.clientModel import Client
from models.userModel import User
from database import db
from models.internetModel import Internet
from models.meetingModel import Meeting
from models.clientOfficeModel import ClientOffice
from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError

"""
This file contains routes for entering client data 
"""

client_bp = Blueprint('client_bp', __name__)

@client_bp.route('/', methods=['POST'])
def userLogin():
    """
    Endpoint for user to login in to the system
    """
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'message': 'No data provided'
        }), 400
    name = data.get('user_name')
    password = data.get('password')
    
    existing_user = db.session.execute(db.select(User).filter_by(user_name=name)).scalar_one_or_none()
    if existing_user and existing_user.check_password(password):
        return jsonify({
            'success': True,
            'message': 'Login successful'
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid username or password'
        }), 401



@client_bp.route('/salesdetails', methods=['POST'])
def salesOffice():
    """
    This endpoint if for fetching user data and saving it in the database
    """

    data = request.get_json()
    if not data:
        return (jsonify({ 
            "success": False,
            "message": 'No data provided'
          }), 400)
    
    client_name = data.get('client_name')
    client_contact = data.get('contact')
    client_email = data.get('client_email')
    job_title = data.get('job')
    deal_information = data.get('deal_info')
    date = data.get('meetingDate')
    location = data.get('meetingLocation')
    type_of_meeting = data.get('meetingType')
    remarks = data.get('meetingRemarks')
    status = data.get('meetingStatus')
    isp_connected = data.get('is_connected')
    isp_name = data.get('isp_name')
    net_connection_type = data.get('connection_type')
    product = data.get('product')
    net_price = data.get('net_price')
    deal_status = data.get('deal_status')
    office_name = data.get('office_name')
    staff_number = data.get('number_staff')
    industry_category = data.get('industry')
    

    new_client = Client(client_name = client_name, 
                        client_contact = client_contact, 
                        client_email=client_email, 
                        job_title = job_title,
                        deal_information = deal_information)
    
    new_meeting = Meeting(meeting_date = date, 
                          meeting_location = location,
                          meetingtype = type_of_meeting,
                          meeting_remarks = remarks,
                          meeting_status = status,
                          attends = new_client)
    

    
    new_internet = Internet(is_isp_connected = isp_connected,
                            isp_name = isp_name,
                            internet_connection_type = net_connection_type,
                            service_provided = product,
                            isp_price = net_price,
                            deal_status = deal_status,
                            hasinternet = new_client)
    
    new_office = ClientOffice(office_name = office_name,
                        staff_number = staff_number,
                        industry_category = industry_category,
                        owns = new_client)
        
    try:
        db.session.add_all([new_client, new_meeting, new_internet, new_office])
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Client information added successfully'
        }), 201
       
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f"Integrity error: {e.orig}"
        })
        
    except DataError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f"Data error: {e.orig}"
        }), 400

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f"Unexpected database error occured \n {e}"
        }), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failure in adding the information {e}'
        }), 500


@client_bp.route('/listclients', methods=['GET'])
def client_data():
    """
    Displays a lists of clients from the database
    """

    client_data = []
    meeting_data = []
    internet_data = []
    office_data = []

    client_list = db.session.execute(db.select(Client).order_by(Client.timestamp)).scalars().all()
    meeting_list = db.session.execute(db.select(Meeting).order_by(Meeting.timestamp)).scalars().all()
    internet_list = db.session.execute(db.select(Internet).order_by(Internet.timestamp)).scalars().all()
    office_list = db.session.execute(db.select(ClientOffice).order_by(ClientOffice.timestamp)).scalars().all()

    for client in client_list:
        client_data.append(client.to_dict())
    
    for meeting in meeting_list:
        meeting_data.append(meeting.to_dict())

    for internet in internet_list:
        internet_data.append(internet.to_dict())
    
    for office in office_list:
        office_data.append(office.to_dict())

    return jsonify({
        'success': True,
        'clients': client_data,
        'meetings': meeting_data,
        'internet': internet_data,
        'offices': office_data
    }), 200


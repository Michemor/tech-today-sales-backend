from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.clientModel import Client
from models.userModel import User
from models.adminModel import Admin
from database import db
from models.internetModel import Internet
from models.meetingModel import Meeting
from models.officeModel import Office
from sqlalchemy.exc import IntegrityError, DatabaseError, DataError, SQLAlchemyError

"""
This file contains routes for entering client data 
"""

client_bp = Blueprint('client_bp', __name__, template_folder='templates',
                      static_folder='static')

@client_bp.route('/', methods=['POST', 'GET'])
def userLogin():
    """
    Endpoint for user to login in to the system
    """
    if request.method == "POST":
        name = request.form.get('username')
        password = request.form.get('password')

        existing_user = db.session.execute(db.select(User).filter_by(user_name=name)).scalar_one_or_none()

        if existing_user and existing_user.check_password(password):
            flash('You have logged in successfully', 'success')
            return redirect(url_for('client_bp.salesOffice'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')


@client_bp.route('/sales', methods=['GET', 'POST'])
def salesOffice():
    """
    This endpoint if for fetching user data and saving it in the database
    """

    if request.method == 'POST':

        provider = None
        net_price = 0
        net_connection_type = None
        product = None
        deal_status = None

        # fetching form data
        client_name = request.form.get('client_name')
        client_email = request.form.get('client_email')
        client_contact = request.form.get('client_contact')
        job_title = request.form.get('job_title')
        deal_information = request.form.get('conversation')

        office_name = request.form.get('office_name')
        staff_number = request.form.get('staff_number')
        industry_category = request.form.get('industry')

        if industry_category == 'Other':
            industry_category = request.form.get('other_industry')

        date = request.form.get('meeting_date')
        location = request.form.get('meeting_location')
        remarks = request.form.get('meeting_remarks')
        status = request.form.get('meeting_status')

        if status == 'other':
            status = request.form.get('other_status')

        isp_connected = request.form.get('net_connected')

        if isp_connected == 'Yes':
            isp_connected = True
            provider = request.form.get('provider')
            if provider == 'Other':
                provider = request.form.get('other-provider')
            
            net_price = request.form.get('price')
            if net_price == 'Other':
                net_price = request.form.get('other_price')
            
            net_connection_type = True if request.form.get('net_connection_type') == 'on' else False

            product = request.form.get('product')

            if product == 'other':
                product = request.form.get('other_product')

            deal_status = request.form.get('deal_status')

            if deal_status == 'Other':
                deal_status = request.form.get('other_deal_status')
        
        else:
            isp_connected = False
        
        new_client = Client(client_name = client_name, client_contact = client_contact, 
                            client_email=client_email, 
                            job_title = job_title,
                            deal_information = deal_information)
        
        new_meeting = Meeting(meeting_date = date, 
                              meeting_location = location,
                              meeting_remarks = remarks,
                              meeting_status = status,
                              attends = new_client)
        
        if provider:
            isp_name = provider
        else:
            isp_name = None
        
        new_internet = Internet(is_isp_connected = isp_connected,
                                isp_name = isp_name,
                                internet_connection_type = net_connection_type,
                                service_provided = product,
                                isp_price = net_price,
                                deal_status = deal_status,
                                hasinternet = new_client)
        
        new_office = Office(office_name = office_name,
                            staff_number = staff_number,
                            industry_category = industry_category,
                            owns = new_client)
        
        try:
            db.session.add_all([new_client, new_meeting, new_internet, new_office])
            db.session.commit()
            flash(f'Entities created successfully', 'success')
            return render_template('results.html')
        except IntegrityError as e:
            db.session.rollback()
            flash(f'Failed to add information due to data conflict or missing data\n {e}', 'error')
            return render_template('client.html')
        
        except DataError as e:
            db.session.rollback()
            flash(f'Invalid data format \n {e}', 'error')
            return render_template('client.html')
        
        except SQLAlchemyError as e:

            db.session.rollback()
            flash(f'Unexpected database error occured \n {e}')
        
        except Exception as e:
            db.session.rollback()
            flash(f'Failure in adding the information {e}')
            return render_template('client.html')
    
    return render_template('client.html')

@client_bp.route('/list')
def client_data():
    """
    Displays a lists of clients from the database
    """

    clients = db.session.execute(db.select(Client).order_by(Client.created_at)).scalars().all()
    return render_template('results.html', clients=clients)


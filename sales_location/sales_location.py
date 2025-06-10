from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.buildingModel import Building
from models.office import BuildingOffice
from database import db
from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError

"""
File containing blueprint and endpoints for sales locations
"""

location_bp = Blueprint('location_bp',
                        __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/sales_location/static/css')

@location_bp.route('/locations', methods=['GET', 'POST'])
def addLocation():
    """
    Endpoint for fetching data from form and sending to database
    """

    if request.method == 'POST':
        building_name = request.form.get('building-name')
        is_fibre = request.form.get('fibre-val')
        number_offices = request.form.get('num-offices')

        if is_fibre != 'Yes' and is_fibre != 'No':
            is_fibre = 'Can connect to MyISP Base Station'

        office_name = request.form.get('office-name')
        office_floor = request.form.get('office-floor')
        other_offices = request.form.get('other-offices')

        ease_access = request.form.get('level')

        access_info = request.form.get('access-info')

        
        existing_building = db.session.execute(
            db.select(Building).filter_by(building_name=building_name)
        ).scalar_one_or_none()

        if existing_building:
           
            current_building = existing_building
            flash(f"Building '{building_name}' already exists. Adding office to it.")
        else:
            
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
            flash('Building and Office created successfully!')
            return render_template('/templates/base.html')

        except IntegrityError as e:
            db.session.rollback()
            flash(f'Database Integrity Error: {e.orig}') 
            return render_template('sales_location.html')

        except DataError as e:
            db.session.rollback()
            flash(f'Database Data Error: {e}')
            return render_template('sales_location.html')

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'SQLAlchemy Error: {e}')
            return render_template('sales_location.html')

        except Exception as e:
            db.session.rollback()
            flash(f'An unexpected error occurred: {e}')
            return render_template('sales_location.html')

    return render_template('sales_location.html')

@location_bp.route('/listsites')
def listLocations():
    """
    List the offices and buildings
    """

    buildings = db.session.execute(db.select(Building).order_by(Building.building_id)).scalars().all()
    offices = db.session.execute(db.select(BuildingOffice).order_by(BuildingOffice.office_id)).scalars().all()

    return render_template('lists.html', buildings=buildings, offices=offices)
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
                        static_folder='static')

@location_bp.route('/locations', methods=['GET', 'POST'])
def addLocation():
    """
    Endpoint for fetching data from form and sending to database
    """

    if request.method == 'POST':
        
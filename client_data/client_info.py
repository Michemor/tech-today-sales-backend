from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.clientModel import Client
from models.userModel import User
from database import db

"""
This file contains routes for entering client data 
"""

client_bp = Blueprint('client_bp', __name__, template_folder='templates')



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
            return redirect(url_for('client'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')


@client_bp.route('/client', methods=['POST', 'GET'])
def client():
    """
    This endpoint if for fetching user data and saving it in the database
    """
    if request.method == 'POST':
        pass
    
    return render_template('client.html')


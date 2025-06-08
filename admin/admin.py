from flask import Blueprint, request, flash, url_for, render_template, redirect
from database import db
from models.userModel import User

admin_bp = Blueprint('admin_bp',  __name__, template_folder='templates')

@admin_bp.route('/users')
def home():
    """ Root route
    """
    added_users = db.session.execute(db.select(User).order_by(User.created_at)).scalars().all()
    return render_template('listuser.html', users=added_users)


@admin_bp.route('/add', methods = ['GET', 'POST'])
def addUser():
    """
    adds new users to the system
    an admin function
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        # check whether user has already been created
        existing_user = User.query.filter_by(user_name = username).first()
        if existing_user:
            return render_template('listuser.html', error='User already exists')
    
        # create new user
        new_user = User(user_name = username, user_email = email)
        new_user.set_password(password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Added a new user successfully")
            return redirect(url_for('users'))
        except Exception as e:
            return redirect(url_for('users', endpoint=f'Error: {e}'))
 
    return render_template('addUser.html')


@admin_bp.route('/', methods=['POST', 'GET'])
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
from flask import Blueprint, request, flash, url_for, render_template, redirect
from models.adminModel import Admin
from database import db
from models.userModel import User

admin_bp = Blueprint('admin_bp',  __name__, template_folder='templates',
                     static_folder='static')


@admin_bp.route('/admin', methods=['POST', 'GET'])
def userLogin():
    """
    Endpoint for user to login in to the system
    """
    if request.method == "POST":
        name = request.form.get('username')
        password = request.form.get('password')

        existing_admin = db.session.execute(db.select(Admin).filter_by(admin_name=name)).scalar_one_or_none()

        if existing_admin and existing_admin.check_password(password):
            flash('You have logged in successfully', 'success')
            return render_template('listuser.html')
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@admin_bp.route('/users')
def users():
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
            return redirect(url_for('admin_bp.users'))
        except Exception as e:
            flash(f'Failure to add a user. Error: {e}')
            return render_template('listuser.html')
 
    return render_template('addUser.html')

# @admin_bp.route('/admin', methods=['GET', 'POST'])
# def create_admin():
# 
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
# 
#         created_admin = Admin(admin_name = username)
#         created_admin.set_password(password)
# 
#         try:
#             db.session.add(created_admin)
#             db.session.commit()
#             return f'Admin created successfully'
#         except Exception as e:
#             return f'Error in creating database {e}'
#     
#     return render_template('create_admin.html')
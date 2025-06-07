from flask import Flask, flash, redirect, request, render_template, url_for
from database import db
from models.user import User
import click
from flask_migrate import Migrate
from config import Config


"""
This is the main file and contains endpoints for creating the app
and fetching data from the database
"""

migrate = Migrate()

def create_app():
    """
    Instantiates the flask app
    initializes the database with the app
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db, command='migrate')
    
    with app.app_context():
        db.create_all()
        click.echo("Database tables created")
    
    @app.route('/admin')
    def home():
        """ Root route
        """

        added_users = db.session.execute(db.select(User).order_by(User.created_at)).scalars().all()

        return render_template('base.html', users=added_users)
    
    @app.route('/users', methods = ['GET', 'POST'])
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
                return render_template('admin.html', error='User already exists')
        
            # create new user
            new_user = User(user_name = username, user_email = email)
            new_user.set_password(password)

            try:
                db.session.add(new_user)
                db.session.commit()
                flash("Added a new user successfully")
                return render_template("admin.html")
            except Exception as e:
                return render_template("admin.html", error=f"Error in adding user {e}")

     
        return render_template('admin.html')
    
    @app.route('/', methods=['POST', 'GET'])
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
    

    @app.route('/client', methods=['POST', 'GET'])
    def client():

        if request.method == 'POST':
            pass
        

        return render_template('client.html')

    return app


            

if __name__ == "__main__":
    create_app().run()
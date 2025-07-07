from flask import Flask
from database import db
import click
from flask_migrate import Migrate
from config import Config
from models.clientModel import Client
from models.internetModel import Internet
from models.userModel import User
from models.meetingModel import Meeting
from models.office import BuildingOffice
from models.buildingModel import Building
from flask_cors import CORS



# importing blueprints to be registered
from views.client_info import client_bp
from admin.admin import admin_bp
from views.sales_location import location_bp



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
    migrate.init_app(app, db)
    app.register_blueprint(admin_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(location_bp)
    # handles CORS for the app
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    with app.app_context():
        db.create_all()
        click.echo("Database tables created")
    
    return app


if __name__ == "__main__":
    create_app().run()
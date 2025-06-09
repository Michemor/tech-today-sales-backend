from flask import Flask
from database import db
import click
from flask_migrate import Migrate
from config import Config
from models.clientModel import Client
from models.internetModel import Internet
from models.userModel import User
from models.officeModel import ClientOffice
from models.meetingModel import Meeting

# importing blueprints to be registered
from client_data.client_info import client_bp
from admin.admin import admin_bp



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

    with app.app_context():
        db.create_all()
        click.echo("Database tables created")
    
    return app


if __name__ == "__main__":
    create_app().run()
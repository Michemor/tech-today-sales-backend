import os
from dotenv import load_dotenv

# this loads environmental variables from .env
load_dotenv()

class Config:
    """
    Contains configurations for main.py file
    Configurations include: database connection string,
                            secret key and track modifications
    """

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
   
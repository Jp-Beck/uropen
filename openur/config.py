# openur/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # This will load the .env file variables into the environment

class Config:
    # This is the secret key for the website. It is used to protect against CSRF attacks.
    SECRET_KEY = os.getenv('SECRET_KEY')
    # configure the SQLite database, relative to the app instance folder
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    # create the mail instance
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # set the email address and password
    MAIL_USERNAME =  os.getenv('EMAIL_USER')
    MAIL_PASSWORD =  os.getenv('EMAIL_PASS')
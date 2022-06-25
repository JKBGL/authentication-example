import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv('APP_NAME')
APP_DESC = os.getenv('APP_DESC')
SQL_URI = os.getenv('SQL_URI')
SECRET_KEY = os.getenv('SECRET_KEY')
APP_VERSION = "0.0.5"
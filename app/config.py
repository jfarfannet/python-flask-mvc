# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-por-defecto'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///food_delivery.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RESTAURANTS_PER_PAGE = 9
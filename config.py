import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma_chave_secreta_muito_segura'
    SQLALCHEMY_DATABASE_URI = os.environ.get('postgresql://finplan_user:123@localhost:5232/finplan_db') or 'postgresql://finplan_user:123@localhost:5232/finplan'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123@localhost:5432/finplan?client_encoding=utf8'
    

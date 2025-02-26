from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://finplan_user:123@localhost:5232/finplan_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Importe os modelos aqui
    from . import models

    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados

    return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Cria a instância do SQLAlchemy

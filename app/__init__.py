from flask import Flask
from flasgger import Swagger

from .extensions import db  # Importe o db do extensions.py

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://finplan_user:123@localhost:5232/finplan_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
    Swagger(app)

    # Inicializa o db com a aplicação
    db.init_app(app)
    

    # Registra as rotas (Blueprints)
    from .routes import main
    app.register_blueprint(main)

    return app
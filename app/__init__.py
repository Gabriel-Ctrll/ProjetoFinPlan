from flask import Flask
from .extensions import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://finplan_user:123@localhost:5232/finplan_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

  
    db.init_app(app)  # Inicializa o SQLAlchemy com a aplicação

    # Importação e registro dos Blueprints
    from .routes import main
    from .auth import auth

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    

    return app

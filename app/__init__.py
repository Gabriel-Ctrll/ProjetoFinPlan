# app/__init__.py
from flask import Flask, request
from .extensions import db, csrf, login_manager
from .models.user import User
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app(config_object="app.config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    
    # Inicialização de extensões
    db.init_app(app)
    csrf.init_app(app)
    
    # Configuração para evitar cache de respostas da API
    @app.after_request
    def add_header(response):
        # Prevenir cache para endpoints de API e arquivos JS
        if request.path.startswith(('/dashboard/', '/categories/')) or request.path.endswith('.js'):
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        return response
    
    # Login manager setup
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'warning'
    
     # Adicione este trecho
    from flask_wtf import FlaskForm
    @app.context_processor
    def inject_form():
        return {'form': FlaskForm()}
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Registro de blueprints
    from .blueprints.auth.routes import auth_bp
    from .blueprints.main.routes import main_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    
    # Inicialização do banco de dados
    with app.app_context():
        db.create_all()
    
    return app

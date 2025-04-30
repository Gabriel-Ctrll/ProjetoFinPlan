# app/__init__.py
from flask import Flask, request
from .extensions import db, csrf, login_manager
from .models.user import User
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app(config_object="app.config.DevelopmentConfig"):
    """
    Factory function para criar uma instância da aplicação Flask.
    
    Esta função inicializa a aplicação Flask, configura todas as extensões,
    registra os blueprints e configura outros aspectos como gerenciamento de
    sessão, CSRF e tratamento de resposta.
    
    Args:
        config_object (str): Caminho para o objeto de configuração a ser usado.
        
    Returns:
        Flask: Uma instância configurada da aplicação Flask.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)

    
    # Inicialização de extensões
    db.init_app(app)
    csrf.init_app(app)
    
    # Configuração para evitar cache de respostas da API
    @app.after_request
    def add_header(response):
        """
        Adiciona headers para prevenir cache em endpoints específicos.
        
        Esta função é executada após cada requisição, adicionando headers
        que previnem o cache de respostas para endpoints de API e arquivos JS.
        
        Args:
            response: O objeto de resposta Flask.
            
        Returns:
            response: O objeto de resposta modificado.
        """
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
        """
        Injeta um formulário vazio em todos os templates.
        
        Esta função permite que todos os templates tenham acesso a
        um objeto form vazio por padrão.
        
        Returns:
            dict: Um dicionário com o objeto form.
        """
        return {'form': FlaskForm()}
    
    @app.context_processor
    def utility_processor():
        """
        Injetar funções Python úteis para templates.
        
        Returns:
            dict: Um dicionário com funções úteis.
        """
        return {
            'abs': abs,  # Permite usar abs() nos templates
        }
    
    @login_manager.user_loader
    def load_user(user_id):
        """
        Carrega um usuário a partir do ID para o Flask-Login.
        
        Args:
            user_id: ID do usuário a ser carregado.
            
        Returns:
            User: O objeto de usuário correspondente ao ID.
        """
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

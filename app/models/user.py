from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from datetime import datetime

class User(UserMixin, db.Model):
    """
    Modelo de Usuário.
    
    Representa um usuário do sistema, com capacidade de autenticação
    e relacionamentos com suas transações e categorias.
    
    Attributes:
        id (int): Identificador único do usuário.
        username (str): Nome de usuário, único no sistema.
        email (str): Email do usuário, único no sistema.
        password_hash (str): Hash da senha do usuário.
        created_at (DateTime): Data e hora de criação da conta.
        transactions (relationship): Relação com as transações do usuário.
        categories (relationship): Relação com as categorias do usuário.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    transactions = db.relationship("Transaction", backref="user", lazy=True)
    categories = db.relationship("Category", backref="user", lazy=True)

    def set_password(self, password):
        """Define a senha do usuário, armazenando apenas o hash."""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'
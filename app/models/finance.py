from app.extensions import db
from datetime import datetime

class Transaction(db.Model):
    """
    Modelo de Transação Financeira.
    
    Representa uma transação financeira realizada pelo usuário, que pode ser
    uma receita ou uma despesa, dependendo da categoria associada.
    
    Attributes:
        id (int): Identificador único da transação.
        user_id (int): ID do usuário que criou a transação.
        category_id (int): ID da categoria associada à transação.
        amount (Numeric): Valor da transação.
        description (str): Descrição da transação.
        date (Date): Data em que a transação ocorreu.
        created_at (DateTime): Data e hora de criação do registro.
        updated_at (DateTime): Data e hora da última atualização.
        notes (Text): Observações adicionais sobre a transação.
    """
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.Text)  # Coluna adicionada pelo script add_notes_column.py

    def __repr__(self):
        return f'<Transaction {self.description}: {self.amount}>'

class Category(db.Model):
    """
    Modelo de Categoria de Transação.
    
    Representa uma categoria que pode ser associada a transações financeiras,
    permitindo classificá-las como receitas ou despesas.
    
    Attributes:
        id (int): Identificador único da categoria.
        name (str): Nome da categoria.
        type (str): Tipo da categoria ('income' ou 'expense').
        user_id (int): ID do usuário que criou a categoria.
        is_income (bool): Indica se a categoria é de receita (True) ou despesa (False).
        transactions (relationship): Relação com as transações desta categoria.
    """
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # "income" ou "expense"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    is_income = db.Column(db.Boolean, nullable=False)  

    transactions = db.relationship("Transaction", backref="category", lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'

# Removida a classe Bank
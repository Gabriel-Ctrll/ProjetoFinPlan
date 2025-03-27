from app.extensions import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    # Removido: bank_id
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.Text)  # Coluna adicionada pelo script add_notes_column.py

    def __repr__(self):
        return f'<Transaction {self.description}: {self.amount}>'

class Category(db.Model):
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
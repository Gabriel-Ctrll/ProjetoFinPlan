from sqlalchemy import Column, Integer, String
from .database import Base  # Importe Base de um módulo separado

from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)


from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    db.session.execute('ALTER TABLE transactions ADD COLUMN IF NOT EXISTS notes TEXT')
    db.session.commit()
    print("Coluna 'notes' adicionada com sucesso!")

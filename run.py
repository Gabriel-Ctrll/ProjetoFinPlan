# run.py

from app import create_app

# Cria a aplicação Flask
app = create_app()

if __name__ == '__main__':
    # Inicia o servidor Flask
    app.run(debug=True)
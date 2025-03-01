from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']  # Pegando o nome de usuário do formulário
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        # Verifica se já existe um usuário com esse e-mail
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("E-mail já cadastrado. Tente outro.", "danger")
            return redirect(url_for('auth.register'))

        # Criando um novo usuário
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Cadastro realizado com sucesso! Faça login.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('main.dashboard'))  # Direciona para o dashboard

        flash("E-mail ou senha incorretos", "danger")
        return redirect(url_for('auth.login'))

    return render_template('login.html')
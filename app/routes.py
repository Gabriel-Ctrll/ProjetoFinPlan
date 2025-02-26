from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from .extensions import db  # Importe o db do extensions.py
from .models import User, Transaction, Category

# Cria um Blueprint para as rotas
main = Blueprint('main', __name__)

# Rota inicial
@main.route('/')
def index():
    return render_template('index.html')

# Rota para listar e cadastrar transações
@main.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if request.method == 'POST':
        user_id = 1  # Substitua pela lógica de autenticação

        # Verifique se o usuário existe
        user = User.query.get(user_id)
        if not user:
            flash('Usuário não encontrado!', 'error')
            return redirect(url_for('main.transactions'))

        # Obtenha os dados do formulário
        type = request.form['type']
        amount = float(request.form['amount'])
        category_id = int(request.form['category_id'])
        description = request.form['description']
        date = request.form['date']
        # Crie uma nova transação
        new_transaction = Transaction(
            user_id=user_id,
            type=type,
            amount=amount,
            category_id=category_id,
            description=description,
            date=date
        )

        # Salve no banco de dados
        db.session.add(new_transaction)
        db.session.commit()

        flash('Transação cadastrada com sucesso!', 'success')
        return redirect(url_for('main.transactions'))

    # Liste as transações existentes
    transactions = Transaction.query.filter_by(user_id=1).all()  # Substitua pela lógica de autenticação
    categories = Category.query.all()
    return render_template('transactions.html', transactions=transactions, categories=categories)

# Rota para listar e cadastrar categorias
@main.route('/categories', methods=['GET', 'POST'])
def categories():
    if request.method == 'POST':
        # Obtenha os dados do formulário
        name = request.form['name']
        type = request.form['type']

        # Crie uma nova categoria
        new_category = Category(name=name, type=type)
        db.session.add(new_category)
        db.session.commit()

        flash('Categoria cadastrada com sucesso!', 'success')
        return redirect(url_for('main.categories'))

    # Liste as categorias existentes
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

# Rota para o dashboard
@main.route('/dashboard')
def dashboard():
    # Obtenha os dados para o dashboard
    transactions = Transaction.query.filter_by(user_id=1).all()  # Substitua pela lógica de autenticação
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    balance = total_income - total_expense

    return render_template('dashboard.html', total_income=total_income, total_expense=total_expense, balance=balance)
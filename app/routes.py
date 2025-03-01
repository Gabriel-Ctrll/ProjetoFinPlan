from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from .extensions import db  # Importe o db do extensions.py
from .models import User, Transaction, Category

# Cria um Blueprint para as rotas
main = Blueprint('main', __name__)

# Rota inicial
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/transactions', methods=['GET', 'POST'])
def transactions():
    user_id = 1  # Substituir pela lógica de autenticação

    if request.method == 'POST':
        user = User.query.get(user_id)
        if not user:
            flash('Usuário não encontrado!', 'error')
            return redirect(url_for('main.transactions'))

        amount = float(request.form['amount'])
        category_id = int(request.form['category_id'])
        description = request.form['description']
        date = request.form['date']

        category = Category.query.get(category_id)
        if not category:
            flash('Categoria inválida!', 'error')
            return redirect(url_for('main.transactions'))

        new_transaction = Transaction(
            user_id=user_id,
            amount=amount,
            category_id=category_id,
            description=description,
            date=date
        )

        db.session.add(new_transaction)
        db.session.commit()

        flash('Transação cadastrada com sucesso!', 'success')
        return redirect(url_for('main.transactions'))

    # Se for GET, obtenha as transações e categorias
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    categories = Category.query.all()

    # 🔹 Passando transactions corretamente para o template
    return render_template('transactions.html', transactions=transactions, categories=categories)

# Rota para excluir uma transação
@main.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    
    if not transaction:
        flash('Transação não encontrada!', 'error')
        return redirect(url_for('main.transactions'))
    
    db.session.delete(transaction)
    db.session.commit()
    
    flash('Transação excluída com sucesso!', 'success')
    return redirect(url_for('main.transactions'))

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

# Rota para excluir uma categoria
@main.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    
    if not category:
        flash('Categoria não encontrada!', 'error')
        return redirect(url_for('main.categories'))
    
    # Verifica se há transações vinculadas a essa categoria
    transactions_with_category = Transaction.query.filter_by(category_id=category_id).first()
    if transactions_with_category:
        flash('Não é possível excluir a categoria porque existem transações vinculadas a ela.', 'error')
        return redirect(url_for('main.categories'))
    
    db.session.delete(category)
    db.session.commit()
    
    flash('Categoria excluída com sucesso!', 'success')
    return redirect(url_for('main.categories'))

# Rota para o dashboard
@main.route('/dashboard')
def dashboard():
    income_categories = Category.query.filter_by(is_income=True).all()
    expense_categories = Category.query.filter_by(is_income=False).all()

    total_income = sum(t.amount for t in Transaction.query.filter(Transaction.category_id.in_([c.id for c in income_categories])).all())
    total_expense = sum(t.amount for t in Transaction.query.filter(Transaction.category_id.in_([c.id for c in expense_categories])).all())

    balance = total_income - total_expense

    return render_template("dashboard.html", total_income=total_income, total_expense=total_expense, balance=balance)

@main.route('/categories/data')
def categories_data():
    user_id = 1  # Pegue o ID do usuário autenticado (mudar conforme necessário)
    
    # Buscar apenas categorias que NÃO são receita (is_income = False)
    categories = db.session.query(
        Category.name, 
        db.func.sum(Transaction.amount).label("total")
    ).join(Transaction).filter(
        Transaction.user_id == user_id,
        Category.is_income == False  # Filtrando apenas despesas
    ).group_by(Category.name).all()

    # Convertendo os dados para JSON
    data = {
        "labels": [category.name for category in categories],
        "values": [category.total for category in categories]
    }
    
    return jsonify(data)



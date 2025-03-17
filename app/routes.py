from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from app.extensions import db  # Importe o db do extensions.py
from app.models import User, Transaction, Category
from flask import session
from app.decorators import login_required
import datetime
from sqlalchemy import extract


# Cria um Blueprint para as rotas
main = Blueprint('main', __name__)

# Rota inicial
@main.route('/')
def index():
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))  # Se logado, vai para o Dashboard
    return redirect(url_for("auth.login"))  # Se não, vai para o Login


@main.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():
    user_id = session.get('user_id')  # ID do usuário logado

    if not user_id:
        flash("Erro: usuário não autenticado!", "error")
        return redirect(url_for("auth.login"))

    if request.method == 'POST':
        user = User.query.get(user_id)
        if not user:
            flash('Usuário não encontrado!', 'error')
            return redirect(url_for('main.transactions'))

        amount = float(request.form['amount'])
        category_id = int(request.form['category_id'])
        description = request.form['description']
        date = request.form['date']

        # Filtra a categoria também pelo user_id
        category = Category.query.filter_by(id=category_id, user_id=user_id).first()
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

    # Busca as transações do usuário, ordenadas por data decrescente
    transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.date.desc()).all()
    # Busca as categorias pertencentes ao usuário
    categories = Category.query.filter_by(user_id=user_id).all()

    return render_template('transactions.html', transactions=transactions, categories=categories)

# Rota para excluir uma transação
@main.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    
    if not transaction:
        flash('Transação não encontrada!', 'error')
        return redirect(url_for('main.transactions'))
    
    db.session.delete(transaction)
    db.session.commit()
    
    flash('Transação excluída com sucesso!', 'success')
    return redirect(url_for('main.transactions'))

# # Rota para listar e cadastrar categorias
# @login_required
# @main.route('/categories', methods=['GET', 'POST'])
# def categories():
#     if request.method == 'POST':
#         # Obtenha os dados do formulário
#         name = request.form['name']
#         type = request.form['type']

#         # Crie uma nova categoria
#         new_category = Category(name=name, type=type)
#         db.session.add(new_category)
#         db.session.commit()

#         flash('Categoria cadastrada com sucesso!', 'success')
#         return redirect(url_for('main.categories'))

#     # Liste as categorias existentes
#     categories = Category.query.all()
#     return render_template('categories.html', categories=categories)

@main.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    if request.method == 'POST':
        # Obtenha os dados do formulário
        name = request.form['name']
        cat_type = request.form['type']  # Espera "income" ou "expense"
        
        # Define is_income com base no tipo
        is_income = True if cat_type == 'income' else False

        # Crie a nova categoria (inclua o user_id se as categorias forem por usuário)
        new_category = Category(name=name, type=cat_type, is_income=is_income, user_id=session.get("user_id"))
        db.session.add(new_category)
        db.session.commit()

        flash('Categoria cadastrada com sucesso!', 'success')
        return redirect(url_for('main.categories'))

    # Para GET, lista todas as categorias do usuário (ou todas, se forem globais)
    categories = Category.query.filter_by(user_id=session.get("user_id")).all()
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
@login_required
@main.route('/dashboard')
def dashboard():
    user_id = session.get("user_id")  # Pegando o ID do usuário autenticado

    # Filtra apenas as categorias de receitas e despesas
    income_categories = Category.query.filter_by(is_income=True).all()
    expense_categories = Category.query.filter_by(is_income=False).all()

    # Obtém todas as transações recentes do usuário
    total_income = db.session.query(db.func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.category_id.in_([c.id for c in income_categories])
    ).scalar() or 0  # Se não houver receitas, retorna 0

    total_expense = db.session.query(db.func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.category_id.in_([c.id for c in expense_categories])
    ).scalar() or 0  # Se não houver despesas, retorna 0

    balance = total_income - total_expense  # Calcula o saldo atualizado

    return render_template("dashboard.html", total_income=total_income, total_expense=total_expense, balance=balance)


@main.route('/categories/data')
@login_required
def categories_data():
    user_id = session.get('user_id')
    
    # Busca todas as categorias de despesa
    expense_categories = Category.query.filter_by(is_income=False).all()
    
    labels = []
    values = []
    
    for category in expense_categories:
        labels.append(category.name)
        total = db.session.query(db.func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.category_id == category.id
        ).scalar() or 0
        values.append(float(total))
    
    # Transações sem categoria
    uncategorized_total = db.session.query(
        db.func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == user_id,
        Transaction.category_id.is_(None)
    ).scalar() or 0

    if uncategorized_total > 0:
        labels.append("Sem Categoria")
        values.append(float(uncategorized_total))
    
    data = {"labels": labels, "values": values}
    return jsonify(data)


@main.route('/dashboard/summary')
@login_required
def dashboard_summary():
    user_id = session.get("user_id")

    # Consulta as categorias de receitas e despesas
    income_categories = Category.query.filter_by(is_income=True).all()
    expense_categories = Category.query.filter_by(is_income=False).all()

    # Soma dos valores de transações de receita
    total_income = db.session.query(db.func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.category_id.in_([c.id for c in income_categories])
    ).scalar() or 0

    # Soma dos valores de transações de despesa
    total_expense = db.session.query(db.func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.category_id.in_([c.id for c in expense_categories])
    ).scalar() or 0

    balance = total_income - total_expense

    summary = {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance
    }
    return jsonify(summary)

@main.route('/dashboard/financial_data')
@login_required
def dashboard_financial_data():
    user_id = session.get("user_id")
    current_year = datetime.datetime.now().year

    labels = []
    incomes = []
    expenses = []

    # Lista de IDs das categorias de receita e despesa
    income_category_ids = [c.id for c in Category.query.filter_by(is_income=True).all()]
    expense_category_ids = [c.id for c in Category.query.filter_by(is_income=False).all()]

    # Para cada mês do ano (1 a 12)
    for month in range(1, 13):
        # Formata o nome do mês (ex.: "Jan", "Fev", etc.)
        labels.append(datetime.date(current_year, month, 1).strftime('%b'))
        
        # Soma das receitas do mês
        income_sum = db.session.query(db.func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            extract('year', Transaction.date) == current_year,
            extract('month', Transaction.date) == month,
            Transaction.category_id.in_(income_category_ids)
        ).scalar() or 0
        incomes.append(income_sum)
        
        # Soma das despesas do mês
        expense_sum = db.session.query(db.func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            extract('year', Transaction.date) == current_year,
            extract('month', Transaction.date) == month,
            Transaction.category_id.in_(expense_category_ids)
        ).scalar() or 0
        expenses.append(expense_sum)

    data = {
        "labels": labels,
        "incomes": incomes,
        "expenses": expenses
    }
    return jsonify(data)


@main.route('/dashboard/transactions_data')
@login_required
def transactions_data():
    user_id = session.get('user_id')
    # Obtém as transações recentes do usuário, ordenadas por data decrescente
    transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.date.desc()).limit(10).all()

    # Cria uma lista de dicionários com os dados necessários
    data = []
    for tx in transactions:
        data.append({
            "id": tx.id,
            "date": tx.date.isoformat(),  # Formato ISO para facilitar a conversão no front-end
            "description": tx.description,
            "category": tx.category.name if tx.category else "Sem Categoria",  # Verifica se a categoria existe
            "amount": tx.amount,
            "is_income": tx.category.is_income if tx.category else False  # Adiciona o tipo de transação
        })

    return jsonify(data)
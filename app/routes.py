from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from app.extensions import db  # Importe o db do extensions.py
from app.models import User, Transaction, Category
from flask import session
from app.decorators import login_required


# Cria um Blueprint para as rotas
main = Blueprint('main', __name__)

# Rota inicial
@main.route('/')
def index():
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))  # Se logado, vai para o Dashboard
    return redirect(url_for("auth.login"))  # Se não, vai para o Login

@login_required
@main.route('/transactions', methods=['GET', 'POST'])
def transactions():
    user_id = session.get('user_id')  # Pegamos o ID do usuário logado

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

    # Agora buscamos as transações mais recentes primeiro
    transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.date.desc()).all()
    categories = Category.query.all()

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
@login_required
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


@login_required
@main.route('/categories/data')
def categories_data():
    user_id = session.get("user_id")  # Agora pega o ID do usuário autenticado

    categories = db.session.query(
        Category.name, 
        db.func.sum(Transaction.amount).label("total")
    ).join(Transaction).filter(
        Transaction.user_id == user_id,
        Category.is_income == False  # 🔹 Somente despesas, já que receitas são separadas
    ).group_by(Category.name).all()

    # Garante que o JSON retornado está sempre atualizado
    data = {
        "labels": [category.name for category in categories],
        "values": [float(category.total) for category in categories]  # Converte para float para evitar erros no JavaScript
    }
    
    return jsonify(data)  # 🔹 Retorna um JSON atualizado




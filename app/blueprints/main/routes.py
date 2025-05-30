from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.finance import Transaction, Category  # Removido: Bank
from app.forms.transaction_forms import TransactionForm, CategoryForm
from datetime import datetime, date
from sqlalchemy import extract, func
import calendar
from dateutil.relativedelta import relativedelta
from app.services.financial_analysis import FinancialAnalysisService  # Importar o serviço

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():
    # Verificar se existem categorias
    categories = Category.query.filter_by(user_id=current_user.id).all()
    
    # Verificar se existem categorias antes de mostrar o formulário
    if not categories:
        flash('Você precisa cadastrar pelo menos uma categoria antes de adicionar transações.', 'error')
        return redirect(url_for('main.categories'))
    
    # Inicializar com uma categoria padrão para evitar o erro
    form = TransactionForm()
    form.category.choices = [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        try:
            # Verificar se a categoria pertence ao usuário
            category = Category.query.filter_by(id=form.category.data, user_id=current_user.id).first()
            if not category:
                flash('Categoria inválida.', 'error')
                return redirect(url_for('main.transactions'))
                
            transaction = Transaction(
                description=form.description.data,
                amount=form.amount.data,
                category_id=form.category.data,
                # Removido: bank_id
                date=form.date.data,
                user_id=current_user.id,
                notes=form.notes.data if hasattr(form, 'notes') else None
            )
            
            db.session.add(transaction)
            db.session.commit()
            
            flash('Transação adicionada com sucesso!', 'success')
            return redirect(url_for('main.transactions'))
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao adicionar transação: {str(e)}")
            flash(f'Erro ao adicionar transação: {str(e)}', 'error')
    elif request.method == 'POST':
        # Se o formulário foi enviado mas não é válido
        print(f"Erros de validação: {form.errors}")
        flash('Verifique os dados inseridos.', 'error')
        
    # Buscar as últimas transações do usuário
    transactions = db.session.query(
        Transaction.id,
        Transaction.description,
        Transaction.amount,
        Transaction.date,
        Category.name.label('category_name'),
        Category.is_income
    ).join(Category)\
     .filter(Transaction.user_id == current_user.id)\
     .order_by(Transaction.date.desc())\
     .limit(10).all()
     
    return render_template(
        'transactions.html', 
        form=form, 
        transactions=transactions
    )

@main_bp.route('/transactions/<int:transaction_id>/delete', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    """Rota para excluir uma transação específica"""
    try:
        # Buscar a transação pelo ID e verificar se pertence ao usuário atual
        transaction = Transaction.query.filter_by(
            id=transaction_id, 
            user_id=current_user.id
        ).first_or_404()
        
        # Armazenar informações para mensagem de confirmação
        description = transaction.description
        
        # Excluir a transação
        db.session.delete(transaction)
        db.session.commit()
        
        flash(f'Transação "{description}" excluída com sucesso!', 'success')
        
        # Verificar se a requisição é AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True})
        
        # Redirecionar para a página de transações
        return redirect(url_for('main.transactions'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir transação: {str(e)}', 'error')
        
        # Se for AJAX, retornar erro
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': str(e)}), 500
            
        # Caso contrário, redirecionar com erro
        return redirect(url_for('main.transactions'))

@main_bp.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    form = CategoryForm()
    
    if form.validate_on_submit():
        is_income = form.type.data == 'income'
        category = Category(
            name=form.name.data,
            type=form.type.data,
            is_income=is_income,
            user_id=current_user.id
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash('Categoria adicionada com sucesso!', 'success')
        return redirect(url_for('main.categories'))
        
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('categories.html', form=form, categories=categories)

@main_bp.route('/categories/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.filter_by(id=category_id, user_id=current_user.id).first_or_404()
    
    # Verifique se a categoria possui transações
    if category.transactions:
        flash('Não é possível excluir uma categoria que possui transações.', 'error')
        return redirect(url_for('main.categories'))
    
    db.session.delete(category)
    db.session.commit()
    
    flash('Categoria excluída com sucesso!', 'success')
    return redirect(url_for('main.categories'))

@main_bp.route('/dashboard/summary')
@login_required
def dashboard_summary():
    try:
        today = date.today()
        
        # Total de receitas (usando SQL direto para evitar problemas de tipo)
        income_query = db.session.query(func.coalesce(func.sum(Transaction.amount), 0).label('total'))\
            .join(Category)\
            .filter(Category.is_income == True)\
            .filter(Transaction.user_id == current_user.id)\
            .filter(extract('month', Transaction.date) == today.month)\
            .filter(extract('year', Transaction.date) == today.year)
        
        income = income_query.scalar() or 0
        
        # Total de despesas    
        expense_query = db.session.query(func.coalesce(func.sum(Transaction.amount), 0).label('total'))\
            .join(Category)\
            .filter(Category.is_income == False)\
            .filter(Transaction.user_id == current_user.id)\
            .filter(extract('month', Transaction.date) == today.month)\
            .filter(extract('year', Transaction.date) == today.year)
        
        expense = expense_query.scalar() or 0
        
        # Certifique-se de que os valores são números e não objetos Decimal
        income_float = float(income)
        expense_float = float(expense)
        balance = income_float - expense_float
        
        return jsonify({
            'total_income': income_float,
            'total_expense': expense_float,
            'balance': balance
        })
    except Exception as e:
        print(f"Erro ao calcular resumo financeiro: {str(e)}")
        return jsonify({
            'total_income': 0,
            'total_expense': 0, 
            'balance': 0,
            'error': str(e)
        }), 500

@main_bp.route('/categories/data')
@login_required
def category_data():
    # Busca todas as categorias do usuário (despesas E receitas)
    categories = Category.query.filter_by(user_id=current_user.id).all()
    
    # Para o gráfico de distribuição de gastos, pegamos apenas despesas
    labels = []
    values = []
    category_ids = []  # Adicionamos IDs para o frontend poder selecionar
    
    for category in categories:
        if not category.is_income:  # Filtra apenas despesas
            # Cálculo do total de transações para cada categoria no mês atual
            today = date.today()
            total = db.session.query(func.sum(Transaction.amount))\
                .filter(Transaction.user_id == current_user.id)\
                .filter(Transaction.category_id == category.id)\
                .filter(extract('month', Transaction.date) == today.month)\
                .filter(extract('year', Transaction.date) == today.year)\
                .scalar() or 0
            
            # Só adiciona na lista se houver valores
            if total > 0:
                labels.append(category.name)
                values.append(float(total))
                category_ids.append(category.id)
    
    return jsonify({
        'labels': labels,
        'values': values,
        'ids': category_ids
    })

@main_bp.route('/categories/all')
@login_required
def all_categories():
    """Retorna todas as categorias do usuário atual para preencher o formulário de transações"""
    categories = Category.query.filter_by(user_id=current_user.id).all()
    
    result = []
    for category in categories:
        result.append({
            'id': category.id,
            'name': category.name,
            'type': category.type,
            'is_income': category.is_income
        })
    
    return jsonify(result)

@main_bp.route('/dashboard/financial_data')
@login_required
def financial_data():
    try:
        # Busca os últimos 6 meses de dados
        today = date.today()
        months = []
        incomes = []
        expenses = []
        
        # Mapeamento de meses em português (abreviado)
        meses_abrev = {
            1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
            7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
        }
        
        # Gerar dados para os últimos 6 meses
        for i in range(5, -1, -1):
            # Calcula o mês (atual - i)
            target_date = today - relativedelta(months=i)
            month_name = meses_abrev[target_date.month]  # Nome abreviado do mês em português
            months.append(f"{month_name}/{target_date.year}")
            
            # Receitas do mês (usando func.coalesce para garantir valores zero em vez de NULL)
            income = db.session.query(func.coalesce(func.sum(Transaction.amount), 0))\
                .join(Category)\
                .filter(Category.is_income == True)\
                .filter(Transaction.user_id == current_user.id)\
                .filter(extract('month', Transaction.date) == target_date.month)\
                .filter(extract('year', Transaction.date) == target_date.year)\
                .scalar() or 0
            
            # Despesas do mês
            expense = db.session.query(func.coalesce(func.sum(Transaction.amount), 0))\
                .join(Category)\
                .filter(Category.is_income == False)\
                .filter(Transaction.user_id == current_user.id)\
                .filter(extract('month', Transaction.date) == target_date.month)\
                .filter(extract('year', Transaction.date) == target_date.year)\
                .scalar() or 0
                
            incomes.append(float(income))
            expenses.append(float(expense))
        
        return jsonify({
            'labels': months,
            'incomes': incomes,
            'expenses': expenses
        })
    except Exception as e:
        print(f"Erro ao gerar dados financeiros: {str(e)}")
        return jsonify({
            'labels': [],
            'incomes': [],
            'expenses': [],
            'error': str(e)
        }), 500

@main_bp.route('/dashboard/transactions_data')
@login_required
def transactions_data():
    # Modifica a consulta para garantir todos os campos necessários
    try:
        # Busca as últimas 5 transações do usuário
        transactions = db.session.query(
            Transaction.id,
            Transaction.description,
            Transaction.amount,
            Transaction.date,
            Category.name.label('category'),
            Category.is_income
        ).join(Category)\
         .filter(Transaction.user_id == current_user.id)\
         .order_by(Transaction.date.desc())\
         .limit(5).all()
        
        result = []
        for tx in transactions:
            result.append({
                'id': tx.id,
                'description': tx.description,
                'amount': float(tx.amount),
                'date': tx.date.strftime('%Y-%m-%d'),
                'category': tx.category,
                'is_income': tx.is_income
            })
        
        return jsonify(result)
    except Exception as e:
        print(f"Erro ao buscar transações: {str(e)}")
        return jsonify([])

@main_bp.route('/transactions/data')
@login_required
def transactions_data_table():
    """Rota para obter todas as transações para a tabela"""
    try:
        # Buscar as transações do usuário
        transactions = db.session.query(
            Transaction.id,
            Transaction.description,
            Transaction.amount,
            Transaction.date,
            Category.name.label('category_name'),
            Category.is_income
        ).join(Category)\
         .filter(Transaction.user_id == current_user.id)\
         .order_by(Transaction.date.desc())\
         .all()
        
        result = []
        for tx in transactions:
            result.append({
                'id': tx.id,
                'description': tx.description,
                'amount': float(tx.amount),
                'date': tx.date.strftime('%Y-%m-%d'),
                'category_name': tx.category_name,
                'is_income': tx.is_income
            })
        
        return jsonify(result)
    except Exception as e:
        print(f"Erro ao buscar dados de transações: {str(e)}")
        return jsonify({'error': str(e)}), 500

@main_bp.route('/monthly-analysis', methods=['GET', 'POST'])
@login_required
def monthly_analysis():
    """Rota para a página de análise mensal com PyTorch"""
    selected_date = None
    
    if request.method == 'POST':
        # Obter a data selecionada pelo usuário
        month = int(request.form.get('month', date.today().month))
        year = int(request.form.get('year', date.today().year))
        selected_date = date(year, month, 1)
    
    # Inicializar o serviço de análise financeira
    analysis_service = FinancialAnalysisService()
    
    # Obter dados de comparação de meses
    if selected_date is None:
        analysis_data = analysis_service.compare_months(current_user.id)
    else:
        analysis_data = analysis_service.compare_months(current_user.id, selected_date)
    
    # Lista de meses para o seletor em português
    meses_em_portugues = [
        (1, "Janeiro"), (2, "Fevereiro"), (3, "Março"), 
        (4, "Abril"), (5, "Maio"), (6, "Junho"),
        (7, "Julho"), (8, "Agosto"), (9, "Setembro"),
        (10, "Outubro"), (11, "Novembro"), (12, "Dezembro")
    ]
    
    # Lista de anos para o seletor (últimos 5 anos)
    current_year = date.today().year
    years = list(range(current_year - 4, current_year + 1))
    
    return render_template(
        'monthly_analysis.html', 
        analysis_data=analysis_data,
        months=meses_em_portugues,
        years=years,
        selected_month=selected_date.month if selected_date else date.today().month,
        selected_year=selected_date.year if selected_date else date.today().year
    )

@main_bp.route('/api/monthly-analysis', methods=['POST'])
@login_required
def api_monthly_analysis():
    """API para obter dados de análise mensal em formato JSON"""
    data = request.json
    month = int(data.get('month', date.today().month))
    year = int(data.get('year', date.today().year))
    selected_date = date(year, month, 1)
    
    # Inicializar o serviço de análise financeira
    analysis_service = FinancialAnalysisService()
    
    # Obter dados de comparação de meses
    analysis_data = analysis_service.compare_months(current_user.id, selected_date)
    
    return jsonify(analysis_data)
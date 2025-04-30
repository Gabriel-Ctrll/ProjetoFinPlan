import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from sqlalchemy import extract, func
from app.extensions import db
from app.models.finance import Transaction, Category
import locale

# Tentar configurar o locale para português brasileiro
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil')
    except:
        pass  # Se não conseguir configurar, usará o padrão

# Mapeamento de meses em português
MESES_PT = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro"
}

class FinancialAnalysisModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(FinancialAnalysisModel, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        x = self.layer1(x)
        x = self.relu(x)
        x = self.layer2(x)
        return x

class FinancialAnalysisService:
    def __init__(self):
        self.model = FinancialAnalysisModel(input_size=2, hidden_size=10, output_size=2)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.01)
        self.criterion = nn.MSELoss()
    
    def get_monthly_data(self, user_id, year, month):
        """Obtém receitas e despesas de um mês específico"""
        # Total de receitas
        income_query = db.session.query(func.coalesce(func.sum(Transaction.amount), 0).label('total'))\
            .join(Category)\
            .filter(Category.is_income == True)\
            .filter(Transaction.user_id == user_id)\
            .filter(extract('month', Transaction.date) == month)\
            .filter(extract('year', Transaction.date) == year)
        
        income = float(income_query.scalar() or 0)
        
        # Total de despesas    
        expense_query = db.session.query(func.coalesce(func.sum(Transaction.amount), 0).label('total'))\
            .join(Category)\
            .filter(Category.is_income == False)\
            .filter(Transaction.user_id == user_id)\
            .filter(extract('month', Transaction.date) == month)\
            .filter(extract('year', Transaction.date) == year)
        
        expense = float(expense_query.scalar() or 0)
        
        return {
            'income': income,
            'expense': expense,
            'balance': income - expense
        }
    
    def get_category_data(self, user_id, year, month):
        """Obtém gastos por categoria para um mês específico"""
        category_data = db.session.query(
                Category.name,
                Category.is_income,
                func.sum(Transaction.amount).label('total')
            )\
            .join(Transaction)\
            .filter(Transaction.user_id == user_id)\
            .filter(extract('month', Transaction.date) == month)\
            .filter(extract('year', Transaction.date) == year)\
            .group_by(Category.id, Category.name, Category.is_income)\
            .all()
            
        return [
            {
                'name': item.name, 
                'is_income': item.is_income,
                'amount': float(item.total)
            } 
            for item in category_data
        ]
    
    def analyze_monthly_trend(self, current_month_data, previous_month_data):
        """Analisa a tendência mensal com PyTorch"""
        # Preparar dados para entrada no modelo
        input_tensor = torch.tensor([
            [current_month_data['income'], current_month_data['expense']],
            [previous_month_data['income'], previous_month_data['expense']]
        ], dtype=torch.float32)
        
        # Alvo ideal: manter ou aumentar renda, diminuir despesas
        target_tensor = torch.tensor([
            [current_month_data['income'] * 1.05, current_month_data['expense'] * 0.95],
            [previous_month_data['income'] * 1.05, previous_month_data['expense'] * 0.95]
        ], dtype=torch.float32)
        
        # Treinar o modelo para aprender padrões
        self.model.train()
        for _ in range(100):
            self.optimizer.zero_grad()
            output = self.model(input_tensor)
            loss = self.criterion(output, target_tensor)
            loss.backward()
            self.optimizer.step()
        
        # Avaliar e gerar previsões
        self.model.eval()
        with torch.no_grad():
            predictions = self.model(input_tensor)
            
        # Calcular melhorias e recomendações
        income_trend = ((current_month_data['income'] / previous_month_data['income']) - 1) * 100 if previous_month_data['income'] > 0 else 0
        expense_trend = ((current_month_data['expense'] / previous_month_data['expense']) - 1) * 100 if previous_month_data['expense'] > 0 else 0
        
        # Calcular próximo mês previsto
        next_month_prediction = {
            'income': float(predictions[0][0].item()),
            'expense': float(predictions[0][1].item()),
            'balance': float(predictions[0][0].item() - predictions[0][1].item())
        }
        
        return {
            'income_trend_percentage': income_trend,
            'expense_trend_percentage': expense_trend,
            'next_month_prediction': next_month_prediction,
            'loss': float(loss.item())
        }
        
    def compare_months(self, user_id, selected_date=None):
        """Compara o mês atual com o mês anterior"""
        if selected_date is None:
            selected_date = date.today()
        
        # Obter dados do mês selecionado
        current_month = selected_date.month
        current_year = selected_date.year
        current_month_data = self.get_monthly_data(user_id, current_year, current_month)
        current_month_categories = self.get_category_data(user_id, current_year, current_month)
        
        # Obter dados do mês anterior
        previous_date = selected_date - relativedelta(months=1)
        previous_month = previous_date.month
        previous_year = previous_date.year
        previous_month_data = self.get_monthly_data(user_id, previous_year, previous_month)
        previous_month_categories = self.get_category_data(user_id, previous_year, previous_month)
        
        # Analisar tendência
        trend_analysis = self.analyze_monthly_trend(current_month_data, previous_month_data)
        
        # Formatar os nomes dos meses em português
        current_month_name = f"{MESES_PT[current_month]} {current_year}"
        previous_month_name = f"{MESES_PT[previous_month]} {previous_year}"
        
        return {
            'current_month': {
                'name': current_month_name,
                'data': current_month_data,
                'categories': current_month_categories
            },
            'previous_month': {
                'name': previous_month_name,
                'data': previous_month_data,
                'categories': previous_month_categories
            },
            'trend_analysis': trend_analysis
        } 
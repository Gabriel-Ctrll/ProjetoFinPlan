# app/forms/transaction_forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange

class TransactionForm(FlaskForm):
    description = StringField('Descrição', validators=[
        DataRequired('Descrição é obrigatória'), 
        Length(max=100, message='Descrição deve ter no máximo 100 caracteres')
    ])
    amount = DecimalField('Valor', validators=[
        DataRequired('Valor é obrigatório'),
        NumberRange(min=0.01, message='Valor deve ser maior que zero')
    ])
    category = SelectField('Categoria', coerce=int, validators=[
        DataRequired('Categoria é obrigatória')
    ])
    date = DateField('Data', validators=[
        DataRequired('Data é obrigatória')
    ], format='%Y-%m-%d')
    notes = TextAreaField('Observações', validators=[
        Length(max=500, message='Observações devem ter no máximo 500 caracteres')
    ])

class CategoryForm(FlaskForm):
    name = StringField('Nome', validators=[
        DataRequired('Nome é obrigatório'),
        Length(max=50, message='Nome deve ter no máximo 50 caracteres')
    ])
    type = SelectField('Tipo', choices=[
        ('expense', 'Despesa'),
        ('income', 'Receita')
    ], validators=[DataRequired('Tipo é obrigatório')])
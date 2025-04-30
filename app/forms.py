from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    DecimalField, 
    DateField, 
    SelectField,
    TextAreaField
)
from wtforms.validators import (
    DataRequired, 
    Length, 
    NumberRange,
    Optional
)

class TransactionForm(FlaskForm):
    description = StringField(
        'Descrição',
        validators=[DataRequired()]
    )
    
    amount = DecimalField(
        'Valor',
        validators=[DataRequired()]
    )
    
    date = DateField(
        'Data',
        validators=[DataRequired()]
    )
    
    category = SelectField(
        'Categoria',
        validators=[DataRequired(message='Selecione uma categoria')],
        coerce=int
    )
    
    notes = TextAreaField(
        'Observações',
        validators=[Optional(), Length(max=500)]
    )

class CategoryForm(FlaskForm):
    name = StringField(
        'Nome',
        validators=[
            DataRequired(message='O nome é obrigatório'),
            Length(min=3, max=50, message='O nome deve ter entre 3 e 50 caracteres')
        ]
    )
    
    type = SelectField(
        'Tipo',
        choices=[
            ('expense', 'Despesa'),
            ('income', 'Receita')
        ],
        validators=[DataRequired(message='Selecione o tipo')]
    )
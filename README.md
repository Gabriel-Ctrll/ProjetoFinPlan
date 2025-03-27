# FinPlan - Sistema de Gerenciamento Financeiro Pessoal

## Visão Geral

FinPlan é uma aplicação web para gerenciamento de finanças pessoais, desenvolvida com Python e Flask. O sistema permite que usuários registrem suas receitas e despesas, visualizem relatórios financeiros e acompanhem seu orçamento.

## Estrutura do Projeto

```
ProjetoFinPlan/
├── app/                          # Pasta principal da aplicação
│   ├── __init__.py               # Inicialização da aplicação Flask
│   ├── config.py                 # Configurações da aplicação
│   ├── extensions.py             # Extensões Flask (db, login_manager, etc.)
│   ├── blueprints/               # Blueprints (rotas e controllers)
│   │   ├── auth/                 # Autenticação (login, registro)
│   │   │   └── routes.py         # Rotas de autenticação
│   │   └── main/                 # Funcionalidades principais
│   │       └── routes.py         # Rotas principais da aplicação
│   ├── forms/                    # Formulários Flask-WTF
│   │   ├── auth_forms.py         # Formulários de autenticação
│   │   └── transaction_forms.py  # Formulários de transações e categorias
│   ├── models/                   # Modelos de dados (SQLAlchemy)
│   │   ├── finance.py            # Modelos financeiros (Transaction, Category)
│   │   └── user.py               # Modelo de usuário
│   ├── static/                   # Arquivos estáticos
│   │   ├── css/                  # Estilos CSS
│   │   └── js/                   # Scripts JavaScript
│   │       ├── app.js            # JavaScript global
│   │       ├── dashboard.js      # Scripts do dashboard
│   │       └── transactions.js   # Scripts de transações
│   └── templates/                # Templates HTML (Jinja2)
│       ├── auth/                 # Templates de autenticação
│       ├── base.html             # Template base
│       ├── dashboard.html        # Página principal de dashboard
│       ├── transactions.html     # Página de transações
│       └── categories.html       # Página de categorias
├── run.py                        # Arquivo para iniciar a aplicação
└── add_notes_column.py           # Script para adicionar coluna de notas
```

## Funcionalidades Principais

### 1. Autenticação de Usuários
- Registro de novos usuários
- Login de usuários
- Proteção de rotas (login_required)

### 2. Gerenciamento de Transações
- Cadastro de receitas e despesas
- Categorização de transações
- Visualização em tabela com filtragem
- Exclusão de transações

### 3. Gerenciamento de Categorias
- Criação de categorias personalizadas
- Classificação entre receitas e despesas
- Exclusão de categorias (se não possuírem transações)

### 4. Dashboard Financeiro
- Resumo de receitas, despesas e saldo atual
- Gráfico de distribuição de gastos por categoria
- Gráfico de receitas vs despesas (últimos 6 meses)
- Listagem das transações recentes

## Tecnologias Utilizadas

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript, Tailwind CSS
- **Banco de Dados**: SQLite/SQLAlchemy 
- **Gráficos**: ApexCharts.js
- **Autenticação**: Flask-Login
- **Formulários**: Flask-WTF

## Modelos de Dados

### User (Usuário)
Representa um usuário do sistema.
- `id`: Identificador único
- `username`: Nome de usuário
- `email`: Email do usuário (único)
- `password_hash`: Hash da senha
- `created_at`: Data de criação

### Transaction (Transação)
Representa uma transação financeira (receita ou despesa).
- `id`: Identificador único
- `user_id`: ID do usuário proprietário
- `category_id`: ID da categoria
- `amount`: Valor da transação 
- `description`: Descrição da transação
- `date`: Data da transação
- `notes`: Observações (opcional)
- `created_at`: Data de criação
- `updated_at`: Data de atualização

### Category (Categoria)
Representa uma categoria para classificar transações.
- `id`: Identificador único
- `name`: Nome da categoria
- `type`: Tipo ('income' ou 'expense')
- `is_income`: Boolean indicando se é receita
- `user_id`: ID do usuário proprietário

## Rotas Principais

### Autenticação
- `/login`: Login de usuários
- `/register`: Registro de novos usuários
- `/logout`: Logout do usuário atual

### Dashboard
- `/dashboard`: Página principal do dashboard
- `/dashboard/summary`: API para obter resumo financeiro
- `/dashboard/financial_data`: API para dados do gráfico financeiro
- `/dashboard/transactions_data`: API para listar transações recentes

### Transações
- `/transactions`: Listagem e cadastro de transações
- `/transactions/data`: API para obter dados de transações
- `/transactions/<id>/delete`: Rota para excluir uma transação

### Categorias
- `/categories`: Listagem e cadastro de categorias
- `/categories/all`: API para obter todas as categorias
- `/categories/data`: API para dados do gráfico de categorias
- `/categories/<id>/delete`: Rota para excluir uma categoria

## Como Executar o Projeto

1. Clone o repositório
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Execute a aplicação:
   ```
   python run.py
   ```
4. Acesse no navegador: `http://localhost:5000`

## Scripts de Manutenção

- `add_notes_column.py`: Adiciona a coluna 'notes' à tabela de transações

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

Se você tiver alguma dúvida ou sugestão, entre em contato:

- **Nome:** Israel Ueda Massatoshi
- **Nome:** Gabriel Araújo da Silva
- **GitHub:** [israel_ueda](https://github.com/IsraelUeda)
- **GitHub:** [Gabriel-Ctrll](https://github.com/Gabriel-Ctrll)

## Agradecimentos

- À equipe do Flask por fornecer uma estrutura incrível para desenvolvimento web.
- À comunidade do Bootstrap por tornar o design acessível a todos.
- Aos usuários do FinPlan por ajudarem a melhorar o projeto com feedbacks valiosos.

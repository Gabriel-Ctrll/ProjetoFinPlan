# FinPlan - Seu Planejamento Financeiro Inteligente

O **FinPlan** é uma aplicação web que ajuda os usuários a gerenciar suas finanças de maneira intuitiva e prática. Com uma interface simples e acessível, o FinPlan permite o cadastro de transações, categorização de gastos, visualização de relatórios e muito mais. Inspirado na experiência gamificada do Duolingo, o aplicativo também oferece desafios e recompensas para incentivar o bom gerenciamento financeiro.

---

## Funcionalidades Principais

- **Cadastro de Transações:** Registre suas receitas e despesas de forma rápida e categorizada.
- **Categorização:** Organize suas transações em categorias personalizadas.
- **Dashboard Interativo:** Visualize gráficos e relatórios financeiros para acompanhar sua saúde financeira.
- **Análise Preditiva:** Identifique padrões de gastos e receba sugestões para otimizar suas finanças.
- **Gamificação:** Complete desafios e ganhe recompensas por um bom gerenciamento financeiro.

---

## Tecnologias Utilizadas

- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Backend:** Flask (Python)
- **Banco de Dados:** PostgreSQL
- **Machine Learning:** PyTorch (para análise preditiva)
- **Autenticação e Segurança:** JWT, OAuth
- **Infraestrutura:** AWS ou Google Cloud (para hospedagem e processamento)

---

## Como Executar o Projeto

Siga os passos abaixo para configurar e executar o FinPlan em sua máquina.

### Pré-requisitos

- Python 3.8 ou superior
- PostgreSQL
- Git (opcional)

### Passo a Passo

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/finplan.git
   cd finplan
   ```

2. **Crie um ambiente virtual e ative-o:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados:**

   - Crie um banco de dados no PostgreSQL chamado `finplan_db`.
   - Atualize a URL de conexão no arquivo `config.py`:

     ```python
     SQLALCHEMY_DATABASE_URI = 'postgresql://seu_usuario:sua_senha@localhost:5432/finplan_db'
     ```

5. **Execute as migrações:**

   ```bash
   alembic upgrade head
   ```

6. **Inicie o servidor Flask:**

   ```bash
   python run.py
   ```

7. **Acesse a aplicação:**

   Abra o navegador e acesse:
   ```
   http://localhost:5000/
   ```

---

## Estrutura do Projeto

```
finplan/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── transactions.html
│   │   ├── categories.html
│   │   └── dashboard.html
│   └── ...
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── run.py
├── requirements.txt
└── README.md
```

---


## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## Contato

Se você tiver alguma dúvida ou sugestão, entre em contato:

- **Nome:** Israel Ueda Massatoshi
- **Nome:** Gabriel Araújo da Silva
- **GitHub:** [israel_ueda](https://github.com/IsraelUeda)
- **GitHub:** [Gabriel-Ctrll](https://github.com/Gabriel-Ctrll)

---

## Agradecimentos

- À equipe do Flask por fornecer uma estrutura incrível para desenvolvimento web.
- À comunidade do Bootstrap por tornar o design acessível a todos.
- Aos usuários do FinPlan por ajudarem a melhorar o projeto com feedbacks valiosos.

---

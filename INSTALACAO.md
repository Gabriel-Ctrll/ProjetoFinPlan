# Guia de Instalação - FinPlan

## Visão Geral
Este guia fornece instruções passo a passo para configurar e executar o projeto FinPlan em seu ambiente local.

## Pré-requisitos

### Software Necessário
- **Python 3.8 ou superior**
- **pip** (gerenciador de pacotes Python)
- **Git** (para clonar o repositório)
- **PostgreSQL 12+** (para produção) ou **SQLite** (para desenvolvimento - automático)

### Verificação de Versões
```bash
python --version
pip --version
psql --version
```

## Passo a Passo da Instalação

### 1. Clonar o Repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd ProjetoFinPlan
```

### 2. Configurar Ambiente Virtual
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Configurar Banco de Dados

#### Opção 1: SQLite (Recomendado para Desenvolvimento)
- **Mais fácil**: Não requer configuração adicional
- **Automático**: O banco é criado automaticamente
- **Arquivo**: `finplan_dev.db` será criado na pasta do projeto

#### Opção 2: PostgreSQL (Para Produção)

##### 3.2.1. Criar Banco de Dados
```sql
-- Conectar ao PostgreSQL como superusuário
psql -U postgres

-- Criar usuário
CREATE USER finplan_user WITH PASSWORD '123';

-- Criar banco de dados
CREATE DATABASE finplan_db;

-- Conceder privilégios
GRANT ALL PRIVILEGES ON DATABASE finplan_db TO finplan_user;

-- Conectar ao banco finplan_db
\c finplan_db

-- Conceder privilégios nas tabelas
GRANT ALL ON SCHEMA public TO finplan_user;
```

##### 3.2.2. Verificar Conexão
```bash
psql -U finplan_user -d finplan_db -h localhost
# Digite a senha: 123
```

### 4. Instalar Dependências
```bash
# Para desenvolvimento (SQLite):
pip install -r requirements.txt

# Se tiver problemas com psycopg2 no Windows:
pip install -r requirements-dev.txt
```

### 5. Configurar Variáveis de Ambiente
```bash
# Copiar arquivo de exemplo
cp env.example .env

# Editar arquivo .env com suas configurações
# Windows:
notepad .env
# Linux/Mac:
nano .env
```

**Conteúdo do arquivo .env:**
```env
# Para desenvolvimento (SQLite):
SECRET_KEY=sua-chave-secreta-aqui
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///finplan_dev.db

# Para produção (PostgreSQL):
# DATABASE_URL=postgresql://finplan_user:123@localhost:5432/finplan_db
```

### 6. Executar Migrações do Banco
```bash
# Aplicar migrações existentes
alembic upgrade head
```

### 7. Executar a Aplicação
```bash
python run.py
```

### 8. Acessar a Aplicação
Abra seu navegador e acesse: `http://localhost:5000`

## Estrutura de Arquivos Importantes

```
ProjetoFinPlan/
├── app/
│   ├── __init__.py          # Configuração principal da aplicação
│   ├── config.py            # Configurações de banco e ambiente
│   ├── extensions.py        # Extensões Flask (SQLAlchemy, Login)
│   └── models/              # Modelos de dados
├── alembic/                 # Migrações do banco de dados
├── requirements.txt         # Dependências Python
├── env.example             # Exemplo de variáveis de ambiente
└── run.py                  # Script de inicialização
```

## Solução de Problemas Comuns

### Erro de Conexão com PostgreSQL
- Verifique se o PostgreSQL está rodando
- Confirme as credenciais no arquivo `app/config.py`
- Teste a conexão manualmente com `psql`

### Erro de Dependências
```bash
# Atualizar pip
pip install --upgrade pip

# Reinstalar dependências
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Erro de Migrações
```bash
# Verificar status das migrações
alembic current

# Aplicar migrações pendentes
alembic upgrade head

# Se houver problemas, recriar migrações
alembic revision --autogenerate -m "recriar_migracoes"
alembic upgrade head
```

### Erro de Permissões (Windows)
- Execute o PowerShell como Administrador
- Verifique se o antivírus não está bloqueando

## Configuração de Produção

### Variáveis de Ambiente de Produção
```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=chave-secreta-muito-segura
DATABASE_URL=postgresql://usuario:senha@host:porta/banco
```

### Usando Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:8000 'app:create_app()'
```

## Comandos Úteis

### Desenvolvimento
```bash
# Executar em modo debug
python run.py

# Ver logs em tempo real
tail -f logs/app.log
```

### Banco de Dados
```bash
# Verificar status das migrações
alembic current

# Criar nova migração
alembic revision --autogenerate -m "descricao_da_mudanca"

# Aplicar migrações
alembic upgrade head

# Reverter migração
alembic downgrade -1
```

### Manutenção
```bash
# Limpar cache Python
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

## Suporte

Se encontrar problemas durante a instalação:

1. Verifique se todos os pré-requisitos estão atendidos
2. Consulte a seção "Solução de Problemas Comuns"
3. Verifique os logs da aplicação
4. Abra uma issue no repositório com detalhes do erro

## Próximos Passos

Após a instalação bem-sucedida:

1. Crie uma conta de usuário através da interface web
2. Explore as funcionalidades do sistema
3. Configure suas categorias financeiras
4. Comece a registrar suas transações


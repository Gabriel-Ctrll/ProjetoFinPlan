#!/bin/bash

echo "========================================"
echo "   Instalador FinPlan para Linux/Mac"
echo "========================================"
echo

echo "[1/5] Verificando Python..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERRO: Python não encontrado!"
    echo "Instale Python 3.8+ em: https://python.org"
    exit 1
fi

echo
echo "[2/5] Criando ambiente virtual..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao criar ambiente virtual!"
    exit 1
fi

echo
echo "[3/5] Ativando ambiente virtual..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao ativar ambiente virtual!"
    exit 1
fi

echo
echo "[4/5] Instalando dependências..."
echo "Tentando instalar com requirements.txt..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo
    echo "Problema com psycopg2, tentando requirements-dev.txt..."
    pip install -r requirements-dev.txt
    if [ $? -ne 0 ]; then
        echo "ERRO: Falha ao instalar dependências!"
        exit 1
    fi
fi

echo
echo "[5/5] Configurando banco de dados..."
echo "Copiando arquivo de configuração..."
cp env.example .env 2>/dev/null

echo
echo "========================================"
echo "    Instalação concluída com sucesso!"
echo "========================================"
echo
echo "Para executar a aplicação:"
echo "1. Ative o ambiente virtual: source venv/bin/activate"
echo "2. Execute: python run.py"
echo "3. Acesse: http://localhost:5000"
echo
echo "O banco SQLite será criado automaticamente!"
echo

@echo off
echo ========================================
echo    Instalador FinPlan para Windows
echo    (Versao SQLite - Sem PostgreSQL)
echo ========================================
echo.

echo [1/5] Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.8+ em: https://python.org
    pause
    exit /b 1
)

echo.
echo [2/5] Criando ambiente virtual...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERRO: Falha ao criar ambiente virtual!
    pause
    exit /b 1
)

echo.
echo [3/5] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERRO: Falha ao ativar ambiente virtual!
    pause
    exit /b 1
)

echo.
echo [4/5] Instalando dependencias...
echo Instalando dependencias para desenvolvimento (SQLite)...
echo Incluindo email-validator para validacao de formularios...
pip install -r requirements-dev.txt
if %errorlevel% neq 0 (
    echo.
    echo ERRO: Falha ao instalar dependencias!
    echo Verifique se o pip esta funcionando corretamente.
    pause
    exit /b 1
)

echo.
echo [5/5] Configurando banco de dados...
echo Copiando arquivo de configuração...
copy env.example .env >nul 2>&1

echo.
echo ========================================
echo    Instalacao concluida com sucesso!
echo ========================================
echo.
echo Para executar a aplicacao:
echo 1. Ative o ambiente virtual: venv\Scripts\activate
echo 2. Execute: python run.py
echo 3. Acesse: http://localhost:5000
echo.
echo O banco SQLite sera criado automaticamente!
echo.
echo NOTA: Esta instalacao usa SQLite para desenvolvimento.
echo Para PostgreSQL, consulte o README.md
echo.
pause

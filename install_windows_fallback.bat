@echo off
echo ========================================
echo    Instalador FinPlan para Windows
echo    (Tenta PostgreSQL, fallback SQLite)
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
echo Tentando instalar com PostgreSQL (requirements.txt)...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo Problema com psycopg2, tentando SQLite (requirements-dev.txt)...
    pip install -r requirements-dev.txt
    if %errorlevel% neq 0 (
        echo ERRO: Falha ao instalar dependencias!
        echo Verifique se o pip esta funcionando corretamente.
        pause
        exit /b 1
    )
    echo.
    echo Instalacao SQLite bem-sucedida!
    set DB_TYPE=SQLite
) else (
    echo.
    echo Instalacao PostgreSQL bem-sucedida!
    set DB_TYPE=PostgreSQL
)

echo.
echo [5/5] Configurando banco de dados...
echo Copiando arquivo de configuracao...
copy env.example .env >nul 2>&1

echo.
echo ========================================
echo    Instalacao concluida com sucesso!
echo ========================================
echo.
echo Tipo de banco instalado: %DB_TYPE%
echo.
echo Para executar a aplicacao:
echo 1. Ative o ambiente virtual: venv\Scripts\activate
echo 2. Execute: python run.py
echo 3. Acesse: http://localhost:5000
echo.
if "%DB_TYPE%"=="SQLite" (
    echo O banco SQLite sera criado automaticamente!
    echo.
    echo NOTA: Esta instalacao usa SQLite para desenvolvimento.
    echo Para PostgreSQL, consulte o README.md
) else (
    echo Configure o banco PostgreSQL conforme README.md
)
echo.
pause


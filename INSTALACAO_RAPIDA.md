# 🚀 Instalação Rápida - FinPlan

## ⚠️ Problema Resolvido: psycopg2 no Windows

Se você está tendo problemas com `psycopg2` no Windows, use uma destas opções:

## 🔧 Opção 1: Instalação Automática (Windows)

### Instalador SQLite (Recomendado para desenvolvimento)
1. **Execute o instalador SQLite:**
   ```
   install_windows.bat
   ```

### Instalador com Fallback (Tenta PostgreSQL, depois SQLite)
1. **Execute o instalador com fallback:**
   ```
   install_windows_fallback.bat
   ```

2. **Siga as instruções na tela**

## 🔧 Opção 2: Instalação Manual com SQLite

### Passo 1: Criar Ambiente Virtual
```bash
python -m venv venv
venv\Scripts\activate
```

### Passo 2: Instalar Dependências (SQLite)
```bash
# Use este arquivo se tiver problemas com psycopg2:
pip install -r requirements-dev.txt
```

### Passo 3: Configurar Banco
```bash
# Copie o arquivo de exemplo:
copy env.example .env
```

### Passo 4: Executar
```bash
python run.py
```

## 🔧 Opção 3: PostgreSQL (Para Produção)

Se quiser usar PostgreSQL:

1. **Instale PostgreSQL** em: https://postgresql.org
2. **Configure o banco** conforme instruções no README.md
3. **Use o arquivo original**: `pip install -r requirements.txt`

## 📁 Arquivos de Configuração

- **`requirements.txt`** - Dependências completas (PostgreSQL)
- **`requirements-dev.txt`** - Dependências para desenvolvimento (SQLite)
- **`env.example`** - Configuração de exemplo
- **`install_windows.bat`** - Instalador SQLite Windows (recomendado)
- **`install_windows_fallback.bat`** - Instalador com fallback PostgreSQL→SQLite
- **`install_linux.sh`** - Instalador Linux/Mac

## 🎯 Recomendação

- **Desenvolvimento**: Use SQLite (mais fácil)
- **Produção**: Use PostgreSQL (mais robusto)

## 🚨 Solução do Problema psycopg2

O erro `Failed building wheel for psycopg2-binary` é comum no Windows. As soluções são:

1. **Usar SQLite** (requirements-dev.txt)
2. **Instalar PostgreSQL** e usar requirements.txt
3. **Usar WSL** (Windows Subsystem for Linux)

## ✅ Após a Instalação

1. Acesse: `http://localhost:5000`
2. Crie uma conta de usuário
3. Comece a usar o sistema!

---

**💡 Dica**: Para desenvolvimento, use `install_windows.bat` (SQLite). Para tentar PostgreSQL primeiro, use `install_windows_fallback.bat`!

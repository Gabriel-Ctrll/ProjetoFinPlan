from functools import wraps
from flask import redirect, url_for, session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:  # Verifica se o usuário está autenticado
            return redirect(url_for("auth.login"))  # Redireciona para a página de login
        return f(*args, **kwargs)
    return decorated_function
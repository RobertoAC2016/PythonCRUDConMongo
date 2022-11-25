 #Dependencies
from flask import session, flash, redirect, url_for, render_template
from functools import wraps

def login_required(f):
    """VALIDACION en los Headers para la sesion del usuario"""

    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            sess = session['username']
            return render_template("index.html")
        except Exception:
            flash(f"No cuentas con acceso", category='error')
            return render_template("login.html")
    return decorated
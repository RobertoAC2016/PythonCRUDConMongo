# Dependencies
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from MongoCon import MongoCon


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET','POST'])
def login():
    data = request.form
    mail = None
    pwd = None
    if data:
        mail = data["email"]
        pwd = data["password"]
        row = None
        with MongoCon() as cnx:
            row = cnx.users.find_one({"email":mail})
            if row:
                valida_pwd = check_password_hash(row["password"], pwd)
                if valida_pwd:
                    session["username"] = mail
                    return redirect(url_for("views.index"))
                    # return render_template("index.html")
                else:
                    flash(f"El password no coincide", category='error')
                    return render_template("login.html")
            else:
                flash(f"La cuenta de email {mail} no esta registrada", category='error')
                return render_template("login.html")
    else:
        return render_template("login.html")


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("views.home"))


@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    data = request.form
    mail = None
    name = None
    pwd1 = None
    pwd2 = None
    if data:
        mail = data["email"]
        name = data["firstname"]
        pwd1 = data["password"]
        pwd2 = data["repassword"]
        #usaremos un if anidado
        if len(mail) < 4:
            flash("El Email debe ser mayor a 3 caracteres", category='error')
        elif len(name) < 2:
            flash("First Name debe ser mayor a 1 caracter", category='error')
        elif pwd1 != pwd2:
            flash("El password no es identico en la confirmacion", category='error')
        elif len(pwd1) < 3:
            flash("El password debe ser mayor a 2 caracteres", category='error')
        else:
            rows = None
            with MongoCon() as cnx:
                rows = list(cnx.users.find({"email":mail}))
                if len(rows) > 0:
                    flash(f"La cuenta de email {mail} ya ha sido registrada", category='error')
                else:
                    new_user = {
                        "email": mail,
                        "first_name": name,
                        "password": generate_password_hash(pwd1),
                    }
                    cnx.users.insert_one(new_user)
                    flash("La cuenta ha sido creada exitosamente", category='success')
    return render_template("sign_up.html")
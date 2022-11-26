#dependencies
from datetime import datetime
from flask import Blueprint, flash, render_template, redirect, request, url_for, session
from utils.decorator import login_required
from MongoCon import MongoCon
from bson import ObjectId


views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def home():
    return render_template("home.html")


@views.route('/home', methods=['POST','GET'])
def posthome():
    return render_template("home.html")


@views.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    rows = None
    with MongoCon() as cnx:
        rows = list(cnx.notes.find({}))
        for row in rows:
            row['date'] = row['date'].strftime(f"%Y-%m-%d %H:%M:%S")
    return render_template("index.html", regs=rows)


@views.route('/nuevanota', methods=['GET','POST'])
@login_required
def nuevanota():
    return render_template("formnewnote.html")
    
    
@views.route('/savenote', methods=['POST'])
@login_required
def savenote():
    try:        
        data = request.form
        if data["title"] == None or data["title"] == '':
            flash("La nota no trae titulo", category="error")
            return render_template("formnewnote.html")
        if data["note"] == None or data["note"] == '':
            flash("La nota no trae contenido", category="error")
            return render_template("formnewnote.html")
        if data and data["title"] != '' and data["note"] != '':
            with MongoCon() as cnx:
                usr = cnx.users.find_one({"email":session['username']}, {"_id":False, "first_name": True})
                note = {
                    "title":data['title'],
                    "note":data['note'],
                    "date":datetime.now(),
                    "status":'active',
                    "autor":usr['first_name'],
                }
                cnx.notes.insert_one(note)
    except Exception as ex:
        pass
        flash("No hay datos en el form", category="error")
        print(f"ERROR => {str(ex)}")
    return redirect(url_for('views.index'))


@views.route('/vernota', methods=['POST'])
@login_required
def vernota():
    gid = request.form['gid']
    data = {
        "title":None,
        "note":     None,
        "date":     None,
        "status":   None,
        "autor":    None,
    }
    with MongoCon() as cnx:
        data = cnx.notes.find_one({"_id":ObjectId(gid)})
    return render_template("vernota.html", title = data["title"], note = data["note"], date = data["date"], status = data["status"], autor = data["autor"])


@views.route('/borrarnota', methods=['POST'])
@login_required
def borrarnota():
    try:        
        gid = request.form['gid']
        if gid:
            with MongoCon() as cnx:
                cnx.notes.delete_one({"_id":ObjectId(gid)})
    except Exception as ex:
        pass
        print(f"ERROR => {str(ex)}")
    return redirect(url_for('views.index'))
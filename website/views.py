#dependencies
from flask import Blueprint, render_template
from utils.decorator import login_required


views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def home():
    return render_template("home.html")


@views.route('/index', methods=['GET'])
@login_required
def index():
    print("ENTRO")
    return render_template("index.html")


@views.route('/home', methods=['POST','GET'])
def posthome():
    return render_template("home.html")


# Ahora veamos como pasar valores desde el back de python al front de HTML, asi de facil es pasar valores desde el back al front
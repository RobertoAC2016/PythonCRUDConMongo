from flask import Flask
from website.views import views
from website.auth import auth


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SECRET KEY RANDOM SAMPLE'
    
    app.register_blueprint(views)
    app.register_blueprint(auth)
    
    return app


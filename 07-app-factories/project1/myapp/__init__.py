from flask import Flask, render_template
from myapp.blueprints.main import main
from myapp.blueprints.auth import auth

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app

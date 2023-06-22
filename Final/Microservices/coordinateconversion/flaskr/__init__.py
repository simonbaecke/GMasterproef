from flask import Flask

def create_app():
    app = Flask(__name__)

    from .blueprints import home
    app.register_blueprint(home.bp)

    from .blueprints import coordinateconversion
    app.register_blueprint(coordinateconversion.bp)

    return app


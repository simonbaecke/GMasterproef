from flask import Flask

def create_app():
    app = Flask(__name__)

    from .blueprints import home
    app.register_blueprint(home.bp)

    from .blueprints import subtractabledrainagesurfacearea
    app.register_blueprint(subtractabledrainagesurfacearea.bp)

    return app


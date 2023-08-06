from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)
    from . import endpoints
    app.register_blueprint(endpoints.bp)
    return app

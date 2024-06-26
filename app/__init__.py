from flask import Flask
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix
from app.controllers.upload_controller import api as todo_api


def create_app():
    # app init
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    api = Api(
        app, version='1.0',
        title='Upload API'
    )

    # namesapces
    api.add_namespace(todo_api)

    return app

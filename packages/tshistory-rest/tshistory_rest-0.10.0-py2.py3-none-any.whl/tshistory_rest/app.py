from flask import Flask

from tshistory_rest.blueprint import httpapi


def make_app(tsa, apiclass=httpapi):
    app = Flask(__name__)
    api = apiclass(tsa)
    app.register_blueprint(
        api.bp
    )
    return app

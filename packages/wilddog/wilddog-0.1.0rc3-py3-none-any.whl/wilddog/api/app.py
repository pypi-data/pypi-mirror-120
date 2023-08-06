from typing import cast

import flask

import wilddog.api.exceptions
from wilddog import config
from wilddog.api.metadata import v0 as metadata
from wilddog.api.projects import v0 as projects


def make_app() -> flask.Flask:
    cfg: config.FlaskConfig = config.wild_dog.flask
    app = flask.Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(SECRET_KEY=cfg["secret_key"])
    app.url_map.strict_slashes = False

    @app.errorhandler(wilddog.api.exceptions.ApiException)
    def handle_api_exception(e: Exception) -> flask.Response:
        err = cast(wilddog.api.exceptions.ApiException, e)
        return err.to_response()

    app.register_blueprint(projects.v0)
    app.register_blueprint(metadata.v0)

    return app

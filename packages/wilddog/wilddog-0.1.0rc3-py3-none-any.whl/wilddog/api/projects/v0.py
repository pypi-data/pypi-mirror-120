from typing import cast

import flask

from wilddog import types
from wilddog.api import response
from wilddog.api.projects import service

v0 = flask.Blueprint("projects", __name__, url_prefix="/projects")


@v0.route("", methods=["GET"])
def projects() -> flask.Response:
    project_list = service.entries()
    return flask.jsonify(project_list)


@v0.route("", methods=["POST"])
def create() -> flask.Response:
    payload = cast(types.Project, flask.request.get_json())
    project_id = service.create(payload)
    r = response.BasicResponse[int](
        status=201, message="Project creation successful", data=project_id
    )
    return r.to_response()

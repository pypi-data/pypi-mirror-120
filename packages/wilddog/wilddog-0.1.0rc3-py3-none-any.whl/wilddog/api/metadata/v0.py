from typing import cast

import flask

from wilddog import types
from wilddog.api import response
from wilddog.api.metadata import service

v0 = flask.Blueprint("metadata", __name__, url_prefix="/metadata")


@v0.route("<int:_id>", methods=["GET"])
def entry(_id: int) -> flask.Response:
    metadata = service.get_entry(_id)
    return flask.jsonify(metadata)


@v0.route("", methods=["POST"])
def create() -> flask.Response:
    metadata = cast(types.MetaData, flask.request.get_json())
    _id = service.create(metadata)
    r = response.BasicResponse[int](status=201, message="Metadata creation successful", data=_id)
    return r.to_response()

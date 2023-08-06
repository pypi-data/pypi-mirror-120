import json
from typing import Dict, Generic, TypeVar

import attr
import flask

T = TypeVar("T")


@attr.s(auto_attribs=True)
class BasicResponse(Generic[T]):
    data: T  # json serializable
    status: int
    message: str
    errors: Dict[str, str] = attr.ib(default=None)

    def jsonify(self) -> str:
        return json.dumps(
            {
                "message": self.message,
                "data": self.data,
                "errors": self.errors,
            }
        )

    def to_response(self) -> flask.Response:
        return flask.Response(
            mimetype="application/json",
            response=self.jsonify(),
            status=self.status,
        )

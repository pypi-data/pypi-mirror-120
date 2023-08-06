import json

import flask


class ApiException(Exception):
    def __init__(self, status: int, error: str) -> None:
        super(ApiException, self).__init__(error)
        self.error = error
        self.status = status

    def to_response(self) -> flask.Response:
        payload = json.dumps({"error": self.error})
        return flask.Response(
            status=self.status,
            response=payload,
            mimetype="application/json",
        )


class UserError(ApiException):
    def __init__(self, error: str) -> None:
        super(UserError, self).__init__(status=400, error=error)


class ObjectNotFound(ApiException):
    def __init__(self, error: str):
        super(ObjectNotFound, self).__init__(status=404, error=error)

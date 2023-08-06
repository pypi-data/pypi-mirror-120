import flask.testing
import pytest
from werkzeug import test as t

from wilddog.models import metadata, transactions


@pytest.mark.usefixtures("projects_list")
def test_list_projects(client: flask.testing.FlaskClient) -> None:
    res: t.TestResponse = client.get("/projects")
    assert res.status_code == 200
    response = res.json
    assert len(response) == 3


@pytest.mark.usefixtures("database_init")
def test_create_project(client: flask.testing.FlaskClient) -> None:
    payload = {"name": "HAT", "description": "The Hat Project"}
    res = client.post("/projects", json=payload)
    assert res.status_code == 201

    # cleanup
    with transactions.Session() as s:
        p = s.query(metadata.Project).first()
        s.delete(p)


@pytest.mark.usefixtures("projects_list")
def test_create__failure(client: flask.testing.FlaskClient):
    payload = {"name": "HAT", "description": "The Hat Project"}
    res = client.post("/projects", json=payload)

    assert res.status_code == 400
    assert "error" in res.json

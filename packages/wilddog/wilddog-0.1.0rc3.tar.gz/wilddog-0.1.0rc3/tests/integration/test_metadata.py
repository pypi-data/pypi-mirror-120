from collections.abc import Iterable
from typing import List

import flask.testing

from wilddog import types


def test_create_metadata(
    projects_list: Iterable[int], client: flask.testing.FlaskClient, database_init
) -> None:

    for project in projects_list:
        m = types.MetaData(
            name=f"{project}-Homes",
            description="Simple valid homes",
            image="https://avatars.githubusercontent.com/u/892017?v=4",
            project_id=project,
            external_urls=[
                {"youtube": "https://youtube.com/1"},
                {"twitter": "https://twitter/1"},
            ],
            attributes=[
                types.MetaDataAttribute(name="age", value="20", value_type="Numeric"),
                types.MetaDataAttribute(name="sex", value="male", value_type="String"),
            ],
        )

        res = client.post("/metadata", json=m)
        assert res.status_code == 201


def test_get_entry(
    projects_list: List[int], client: flask.testing.FlaskClient, database_init
) -> None:

    # create
    m = types.MetaData(
        name=f"X-Homes",
        description="Simple valid homes",
        image="https://avatars.githubusercontent.com/u/892017?v=4",
        project_id=projects_list[0],
        external_urls=[{"youtube": "https://youtube.com/1"}, {"twitter": "https://twitter/1"}],
        attributes=[
            types.MetaDataAttribute(name="age", value="20", value_type="Numeric"),
            types.MetaDataAttribute(name="sex", value="male", value_type="String"),
        ],
    )

    res = client.post("/metadata", json=m)
    assert res.status_code == 201

    r = client.get(f"/metadata/{res.json['data']}")
    assert r.status_code == 200
    assert len(r.json["attributes"]) == 2

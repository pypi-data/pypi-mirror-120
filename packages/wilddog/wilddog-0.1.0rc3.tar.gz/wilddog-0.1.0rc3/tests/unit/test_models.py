from wilddog import types
from wilddog.models import metadata


def test_from_dict__project():
    project = types.Project(name="TEST", description="Test project")
    mp = metadata.Project.from_dict(project)
    assert mp.name == "TEST"
    assert mp.description == "Test project"


def test_from_dict__metadata():
    md = types.MetaData(
        name="TXT",
        description="TXT sample",
        image="ipfs://sillyexample",
        external_urls=[{"youtube": "https://youtube.com/1"}, {"twitter": "https://twitter/1"}],
        attributes=[
            types.MetaDataAttribute(name="age", value="20", value_type="Numeric"),
            types.MetaDataAttribute(name="sex", value="male", value_type="String"),
        ],
    )

    meta = metadata.MetaData.from_dict(md)
    assert meta.name == "TXT"
    assert len(meta.external_urls) == 2
    assert len(meta.attributes) == 2

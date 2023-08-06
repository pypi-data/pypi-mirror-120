from wilddog import config
from wilddog.models import metadata, transactions


def test_load_config(settings_file: str) -> None:
    cfg_file = config.WildDogConfigFile(uri=settings_file)
    cfg = cfg_file.load()

    assert cfg.title == "Wild Dog configuration file"
    assert cfg.database["url"] == "postgresql://test:test@localhost:5432/wild_dog"


def test_database_initialization(database_init):
    with transactions.Session() as s:
        p = metadata.Project(name="TEST", description="TEST project")
        s.add(p)

    # get
    with transactions.Session() as s:
        assert s.query(metadata.Project).count() == 1

    # cleanup
    with transactions.Session() as s:
        p = s.query(metadata.Project).filter(metadata.Project.name == "TEST").one()
        s.delete(p)

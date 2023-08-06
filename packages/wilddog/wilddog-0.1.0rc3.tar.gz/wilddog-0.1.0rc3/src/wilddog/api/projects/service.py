from typing import Iterable

from wilddog.api import exceptions
from wilddog.models import metadata, transactions
from wilddog.types import Project


def entries() -> Iterable[Project]:
    with transactions.Session() as s:
        projects = s.query(metadata.Project)
        return [Project(name=p.name, description=p.description) for p in projects]


def create(payload: Project) -> int:
    name = payload["name"]
    with transactions.Session() as s:
        existing = s.query(metadata.Project).filter(metadata.Project.name == name).count()
        if existing:
            raise exceptions.UserError(error=f"A project with name {name} already exists")

        project = metadata.Project.from_dict(payload)
        s.add(project)
        s.flush()

        return project.id

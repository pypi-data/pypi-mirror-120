import logging
from typing import Optional

from wilddog.api import exceptions
from wilddog.models import metadata, transactions
from wilddog.types import MetaData

logger = logging.getLogger(__name__)


def get_entry(_id: int) -> MetaData:

    with transactions.Session() as s:
        m: Optional[metadata.MetaData] = s.query(metadata.MetaData).get(_id)

        if not m:
            raise exceptions.ObjectNotFound(f"No metadata with provided id: {_id} found")
        meta_dict: MetaData = m.as_dict()
        return meta_dict


def create(payload: MetaData) -> int:
    logger.info(f"creating new metadata with name {payload['name']}")
    project_id = payload["project_id"]

    with transactions.Session() as s:
        # get project
        project: Optional[metadata.Project] = s.query(metadata.Project).get(payload["project_id"])

        if not project:
            raise exceptions.UserError(f"Unknown project with id: {project_id} specified")

        # does name exist in project
        existing: int = (
            s.query(metadata.MetaData)
            .filter(
                metadata.MetaData.name == payload["name"],
                metadata.MetaData.project_id == project_id,
            )
            .count()
        )

        if existing > 0:
            raise exceptions.UserError(
                f"A metadata with the same name: {payload['name']} already exist"
            )
        m = metadata.MetaData.from_dict(payload)
        project.entries.append(m)
        s.flush()

        return m.id

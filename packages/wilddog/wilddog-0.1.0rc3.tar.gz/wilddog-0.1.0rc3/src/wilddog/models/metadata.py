from typing import Dict, List, Set, Union, cast

import sqlalchemy as sa
from sqlalchemy import orm

from wilddog import types
from wilddog.models import validators
from wilddog.models.base import BaseEntity

ALLOWED_ATTRS_TYPES: Set[validators.ValueTypeLiteral] = {"String", "Numeric", "Boolean"}


class Project(BaseEntity):
    name: str = sa.Column(sa.String(32), nullable=False, unique=True)
    description: str = sa.Column(sa.String(512), nullable=False)
    entries: List["MetaData"] = orm.relationship(
        "MetaData", cascade="all, delete", backref="project"
    )

    def as_dict(self) -> types.Project:
        return types.Project(
            name=self.name,
            description=self.description,
            entries=[e.as_dict() for e in self.entries],
        )

    @classmethod
    def from_dict(cls, data: types.Project) -> "Project":
        pr = cls()
        pr.name = data["name"]
        pr.description = data["description"]
        return pr


class MetaData(BaseEntity):
    name: str = sa.Column(
        sa.String(32),
        nullable=False,
        comment="Identifies the asset to which this metadata represents",
    )
    description: str = sa.Column(
        sa.String(512),
        nullable=False,
        comment="Describes the asset to which this metadata represents",
    )
    image: str = sa.Column(
        sa.String(256),
        nullable=False,
        comment="A URI pointing to a resource with mime type image/* representing the asset to which this NFT "
        "represents. Consider making any images at a width between 320 and 1080 pixels and aspect ratio "
        "between 1.91:1 and 4:5 inclusive.",
    )

    project_id: int = sa.Column(sa.Integer, sa.ForeignKey("project.id"))
    external_urls: List["ExternalUrl"] = orm.relationship(
        "ExternalUrl", cascade="all, delete", backref="metadata"
    )
    attributes: List["MetaDataAttribute"] = orm.relationship(
        "MetaDataAttribute", cascade="all, delete", backref="metadata"
    )

    def as_dict(self) -> types.MetaData:
        return types.MetaData(
            name=self.name,
            description=self.description,
            image=self.image,
            external_urls=[e.as_dict() for e in self.external_urls],
            attributes=[a.as_dict() for a in self.attributes],
        )

    @classmethod
    def from_dict(cls, data: types.MetaData) -> "MetaData":
        md = cls()
        md.name = data["name"]
        md.description = data["description"]
        md.image = data["image"]

        for e in data.get("external_urls", []):
            md.external_urls.append(ExternalUrl.from_dict(e))
        for a in data.get("attributes", []):
            md.attributes.append(MetaDataAttribute.from_dict(a))
        return md


class ExternalUrl(BaseEntity):
    url: str = sa.Column(sa.String(256), nullable=True, comment="External URL for this metadata")
    name: str = sa.Column(sa.String(256), nullable=True, comment="External URL service name")
    meta_data_id: int = sa.Column(sa.Integer, sa.ForeignKey("metadata.id"))

    def as_dict(self) -> Dict[str, str]:
        return {self.name: self.url}

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "ExternalUrl":
        ex = cls()
        name, url = next(iter(data.items()))
        ex.name = name
        ex.url = url
        return ex


class MetaDataAttribute(BaseEntity):
    name: str = sa.Column(sa.String(128), nullable=False)
    value: str = sa.Column(sa.String(256), nullable=True)
    value_type: validators.ValueTypeLiteral = sa.Column(
        sa.String(16), nullable=False, default="String"
    )

    meta_data_id: int = sa.Column(sa.Integer, sa.ForeignKey("metadata.id"))

    @orm.validates("value_type")
    def validate_value_type(self, name: str, value_type: validators.ValueTypeLiteral) -> str:
        if name != "value_type":
            return value_type

        if value_type not in ALLOWED_ATTRS_TYPES:
            raise ValueError(f"{value_type} not one of the allowed values {ALLOWED_ATTRS_TYPES}")

        if self.value:
            validators.validate(value_type, self.value)
        return value_type

    @orm.validates("value")
    def validate_value(self, name: str, value: str) -> str:
        if name != "value":
            return value

        if self.value_type:
            validators.validate(self.value_type, value)
        return value

    def as_dict(self) -> types.MetaDataAttribute:
        val_type = validators.get_type(self.value_type)
        return types.MetaDataAttribute(
            name=self.name, value=val_type.value_of(self.value), value_type=self.value_type
        )

    @classmethod
    def from_dict(cls, data: types.MetaDataAttribute) -> "MetaDataAttribute":
        md = cls()
        md.name = data["name"]
        md.value = cast(str, data["value"])
        md.value_type = data.get("value_type") or "String"
        return md

from typing import Dict, List, TypedDict, Union

from wilddog.models import validators


class Project(TypedDict, total=False):
    id: int
    name: str
    description: str
    entries: List["MetaData"]


class MetaDataAttribute(TypedDict):
    name: str
    value: Union[bool, float, str]
    value_type: validators.ValueTypeLiteral


class MetaData(TypedDict, total=False):
    id: int
    name: str
    image: str
    description: str
    project_id: int
    external_urls: List[Dict[str, str]]
    attributes: List[MetaDataAttribute]

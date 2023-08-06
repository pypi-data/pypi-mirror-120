from dataclasses import dataclass
from typing import List


@dataclass
class Message:
    id: str
    parent_id: str
    attributes: dict
    content_type: str
    content: bytes

    def __init__(
        self,
        id: str,
        parent_id: str,
        attributes: dict,
        content_type: str,
        content: bytes,
    ):
        self.id = id
        self.parent_id = parent_id
        self.attributes = attributes
        self.content_type = content_type
        self.content = content


@dataclass
class Transfer:
    message: Message
    relation_name: str

    def __init__(self, message: Message, relation_name: str):
        self.message = message
        self.relation_name = relation_name


@dataclass
class Package:
    name: str
    version: str

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version


@dataclass
class Parameter:
    name: str
    title: str
    hint: str
    field_type: str

    def __init__(self, name: str, title: str, hint: str, field_type: str):
        self.name = name
        self.title = title
        self.hint = hint
        self.field_type = field_type


@dataclass
class RelationDesc:
    name: str

    def __init__(self, name: str):
        self.name = name


@dataclass
class Desc:
    title: str
    description: str
    group: str
    parameters: List[Parameter]
    relations: List[RelationDesc]

    def __init__(
        self,
        title: str,
        description: str,
        group: str,
        parameters: List[Parameter],
        relations: List[RelationDesc],
    ):
        self.title = title
        self.description = description
        self.group = group
        self.parameters = parameters
        self.relations = relations

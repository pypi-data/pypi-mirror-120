from typing import Any

from docstring_parser import parser

from grebble_flow.processors import models
from .session import Session


class BaseFlowProcessor:
    def get_package(self) -> models.Package:
        return models.Package(self.name, "")

    def get_description(self) -> models.Desc:
        parameters = []

        docs = parser.parse(self.settings.__doc__)
        for key, value in self.settings.__annotations__.items():
            param_doc = [x for x in docs.params if x.arg_name == key]
            description = ""
            field_type = "str"
            if len(param_doc) > 0:
                param_doc = param_doc[0]
                description = param_doc.description
                field_type = param_doc.type_name

            parameters += [models.Parameter(key, description, description, field_type)]
        return models.Desc(
            title=self.title,
            description=self.description,
            group=self.group,
            relations=self.relations,
            parameters=parameters,
        )

    def on_trigger(self, s: Session, settings: Any, *args, **kwargs):
        raise NotImplemented()

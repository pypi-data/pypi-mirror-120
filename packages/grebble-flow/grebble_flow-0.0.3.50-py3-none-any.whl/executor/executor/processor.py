from dataclasses import dataclass
from typing import Any

from dataclasses_json import dataclass_json
from executor.execsdk import exec_code
from grebble_flow.processors.base import BaseFlowProcessor
from grebble_flow.processors import models
from grebble_flow.processors.session import Session


@dataclass
@dataclass_json
class SimpleFlowSettings:
    """
    Args:
       code (string): Python code
    """

    code: str

    def __init__(self, code):
        self.code = code


class SimpleProcessor(BaseFlowProcessor):
    title = "Python code executor"
    description = "Python code executor"
    name = "python-code-executor"
    group = "python"
    relations = [models.RelationDesc("success")]
    settings = SimpleFlowSettings

    def on_trigger(
        self, session: Session, settings: SimpleFlowSettings, *args, **kwargs
    ):
        return exec_code(settings.code, session)
        # exec(code, {"session": session})

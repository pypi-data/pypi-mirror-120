from typing import List

from xlsx_lib.domain.json_serializable.custom_json_serializable import JSONSerializable
from xlsx_lib.domain.tightening_torques.component_part import ComponentPart


class Component(JSONSerializable):
    name: str
    parts: List[ComponentPart]

    def __init__(self, name: str):
        self.name = name
        self.parts = list()


from typing import List

from xlsx_lib.domain.json_serializable.custom_json_serializable import JSONSerializable

from xlsx_lib.domain.engine.section_element import SectionElement


# TODO: Check if JSONSerializable is needed
class EngineSection(JSONSerializable):
    name: str
    section_elements: List[SectionElement]

    def __init__(
            self,
            name: str,
    ):
        self.name = name
        self.section_elements = list()

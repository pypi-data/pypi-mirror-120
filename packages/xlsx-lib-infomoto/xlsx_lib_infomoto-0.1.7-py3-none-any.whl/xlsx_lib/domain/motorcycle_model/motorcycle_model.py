import random
from typing import Optional, IO, List

from xlsx_lib.domain.engine.engine_section import EngineSection
from xlsx_lib.domain.frame.frame_element import FrameElement
from xlsx_lib.domain.json_serializable.custom_json_serializable import JSONSerializable

from xlsx_lib.domain.generic_replacements.replacement import Replacement
from xlsx_lib.domain.tightening_torques.component import Component
from xlsx_lib.domain.electronic.electronic_element import ElectronicElement


class MotorcycleModel(JSONSerializable):
    def __init__(
            self,
            model_name: str,
            generic_replacements: Optional[List[Replacement]] = None,
            components_screws_tightening_torques: Optional[List[Component]] = None,
            electronic_elements: Optional[List[ElectronicElement]] = None,
            engine_sections: Optional[List[EngineSection]] = None,
            frame_elements: Optional[List[FrameElement]] = None,
            directory_name: Optional[str] = None,
    ):
        self.name: str = model_name
        self.generic_replacements: Optional[List[Replacement]] = generic_replacements
        self.components_screws_tightening_torques: Optional[List[Component]] = components_screws_tightening_torques
        self.electronic_elements: Optional[List[ElectronicElement]] = electronic_elements
        self.engine_sections: List[EngineSection] = engine_sections
        self.frame_elements: Optional[List[FrameElement]] = frame_elements

        json_text: str = self.to_json()

        path: str

        if directory_name is not None:
            path = f"{directory_name}/{self.name}.json"
        else:
            path = f"./xlsx_lib/json/{random.randint(0, 999)}.json"

        file: IO = open(path, "w")
        file.write(json_text)
        file.close()

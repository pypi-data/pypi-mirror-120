from typing import List

from xlsx_lib.domain.generic_replacements.replacement_part import ReplacementPart


# TODO: To dataclass with Optional[list[ReplacementPart]]
class Replacement:
    name: str
    reference: str
    observations: str
    parts: List[ReplacementPart]

    def __init__(self, name: str, reference: str, observations: str):
        self.name = name
        self.reference = reference
        self.observations = observations
        self.parts = list()

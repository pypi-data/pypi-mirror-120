from typing import Optional

from camel_model.camel_model import CamelModel


class ReplacementPart(CamelModel):
    name: str
    reference: str
    observations: Optional[str]

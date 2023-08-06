from typing import List

from xlsx_lib.domain.tightening_torques.tightening_torque_step import TighteningTorqueStep


class ComponentPartScrew:
    def __init__(
            self,
            name: str,
            tightening_torque: str,
            detail: str
    ):
        self.name: str = name
        self.tightening_torque: str = tightening_torque
        self.steps: List[TighteningTorqueStep] = List[TighteningTorqueStep]()
        self.detail: str = detail

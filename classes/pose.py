from typing import List, Any


class Pose:
    """class to save a list of joints wich are represented as a pose"""

    def __init__(self, joints: List) -> None:
        self.joints = joints

    def ToJson(self) -> dict[Any, dict[str, Any]]:
        _dict = {}
        for joint in self.joints:
            _dict[joint.name] = {
                "x": joint.x,
                "y": joint.y,
                "z": joint.z,
                "likelihood": joint.likelihood
            }
        return _dict

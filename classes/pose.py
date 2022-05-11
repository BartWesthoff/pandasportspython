from typing import Set

class Pose:

    def __init__(self, joints: int) -> None:
        self.joints = joints

    def ToJson(self) -> Set(float, float, float, float):
        _dict = {}
        for joint in self.joints:
            _dict[joint.name] = {
                "x": joint.x,
                "y": joint.y,
                "z": joint.z,
                "likelihood": joint.likelihood
            }
        return _dict

from typing import Set, List, Dict, Any

#Klasse voor het opslaan van joints 

class Pose:

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
